"""
Multi-LLM Generation Pipeline for Renode Peripheral Models

This module orchestrates the 6-step multi-LLM pipeline for generating
Renode peripheral models from documentation. It coordinates between
different LLMs, manages pipeline state, and ensures quality through
validation at each step.

Key Features:
- 6-step pipeline orchestration with dedicated LLM calls
- Step-specific prompt engineering with few-shot examples
- Multi-pass validation for critical steps
- Pipeline state management and resumability
- Comprehensive error handling and recovery
- Progress tracking and ETA estimation

Author: Renode Model Generator Team
Version: 2.0.0
"""

import asyncio
import json
import logging
import os
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from enum import Enum
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml

from model_manager import ModelManager, GenerationResult
from validation_engine import ValidationEngine, ValidationResult, Severity
from todo_processor import TodoProcessor
from milvus_rag_handler import MilvusRAGHandler


class PipelineStep(Enum):
    """Pipeline step identifiers."""
    SECTION_SUMMARY = "section_summary"
    DATA_EXTRACTION = "data_extraction"
    REGISTER_MAPPING = "register_mapping"
    ARCHITECTURE_PLANNING = "architecture_planning"
    TODO_GENERATION = "todo_generation"
    CODE_GENERATION = "code_generation"


class PipelineStatus(Enum):
    """Pipeline execution status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    HALTED = "halted"
    RESUMED = "resumed"


@dataclass
class StepResult:
    """Result from a pipeline step."""
    step: PipelineStep
    status: PipelineStatus
    data: Any
    validation_result: Optional[ValidationResult] = None
    generation_result: Optional[GenerationResult] = None
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "step": self.step.value,
            "status": self.status.value,
            "data": self.data,
            "validation_result": self.validation_result.to_dict() if self.validation_result else None,
            "generation_result": {
                "model": self.generation_result.model,
                "confidence_score": self.generation_result.confidence_score,
                "total_tokens": self.generation_result.total_tokens,
                "cost": self.generation_result.cost
            } if self.generation_result else None,
            "error": self.error,
            "timestamp": self.timestamp,
            "retry_count": self.retry_count
        }


@dataclass
class PipelineState:
    """Complete pipeline state for persistence."""
    pipeline_id: str
    peripheral_name: str
    documentation_path: str
    current_step: Optional[PipelineStep] = None
    status: PipelineStatus = PipelineStatus.NOT_STARTED
    step_results: Dict[PipelineStep, StepResult] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_cost: float = 0.0
    total_tokens: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "pipeline_id": self.pipeline_id,
            "peripheral_name": self.peripheral_name,
            "documentation_path": self.documentation_path,
            "current_step": self.current_step.value if self.current_step else None,
            "status": self.status.value,
            "step_results": {
                step.value: result.to_dict() 
                for step, result in self.step_results.items()
            },
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_cost": self.total_cost,
            "total_tokens": self.total_tokens,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PipelineState':
        """Create from dictionary."""
        state = cls(
            pipeline_id=data["pipeline_id"],
            peripheral_name=data["peripheral_name"],
            documentation_path=data["documentation_path"],
            status=PipelineStatus(data["status"]),
            total_cost=data.get("total_cost", 0.0),
            total_tokens=data.get("total_tokens", 0),
            metadata=data.get("metadata", {})
        )
        
        if data.get("current_step"):
            state.current_step = PipelineStep(data["current_step"])
        
        if data.get("start_time"):
            state.start_time = datetime.fromisoformat(data["start_time"])
        
        if data.get("end_time"):
            state.end_time = datetime.fromisoformat(data["end_time"])
        
        # Note: step_results would need to be reconstructed from saved data
        
        return state


class GenerationPipeline:
    """Orchestrates the 6-step multi-LLM pipeline for peripheral generation."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the generation pipeline.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.model_manager = ModelManager(config_path)
        self.validation_engine = ValidationEngine(self.config.get("validation", {}))
        self.todo_processor = TodoProcessor(self.config.get("todo", {}))
        self.rag_handler = None  # Initialize when needed
        
        # Pipeline state
        self.current_state: Optional[PipelineState] = None
        
        # Step definitions with order
        self.step_order = [
            PipelineStep.SECTION_SUMMARY,
            PipelineStep.DATA_EXTRACTION,
            PipelineStep.REGISTER_MAPPING,
            PipelineStep.ARCHITECTURE_PLANNING,
            PipelineStep.TODO_GENERATION,
            PipelineStep.CODE_GENERATION
        ]
        
        # Executor for parallel operations
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Human-in-the-loop flag
        self.human_intervention_enabled = self.config.get("pipeline", {}).get("human_intervention", False)
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Try default config
        default_path = Path("config.yaml")
        if default_path.exists():
            with open(default_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Return minimal config
        return {
            "pipeline": {
                "timeouts": {
                    "default": 120
                },
                "retry": {
                    "max_attempts": 3,
                    "backoff_multiplier": 2,
                    "initial_delay": 5
                }
            },
            "validation": {
                "min_validation_score": 70.0
            }
        }
    
    async def run_pipeline(
        self,
        peripheral_name: str,
        documentation_path: str,
        resume_from: Optional[PipelineStep] = None,
        pipeline_id: Optional[str] = None
    ) -> PipelineState:
        """
        Run the complete generation pipeline.
        
        Args:
            peripheral_name: Name of the peripheral to generate
            documentation_path: Path to peripheral documentation
            resume_from: Optional step to resume from
            pipeline_id: Optional pipeline ID for resuming
            
        Returns:
            Final pipeline state
        """
        self.logger.info(f"Starting pipeline for {peripheral_name}")
        
        # Initialize or load pipeline state
        if pipeline_id and resume_from:
            self.current_state = self._load_pipeline_state(pipeline_id)
            self.current_state.status = PipelineStatus.RESUMED
        else:
            self.current_state = PipelineState(
                pipeline_id=pipeline_id or self._generate_pipeline_id(),
                peripheral_name=peripheral_name,
                documentation_path=documentation_path,
                start_time=datetime.now()
            )
        
        # Load documentation
        documentation = self._load_documentation(documentation_path)
        if not documentation:
            self.current_state.status = PipelineStatus.FAILED
            self.current_state.end_time = datetime.now()
            return self.current_state
        
        # Initialize RAG handler if configured
        if self.config.get("milvus", {}).get("host"):
            try:
                self.rag_handler = MilvusRAGHandler(self.config)
                await self.rag_handler.connect()
            except Exception as e:
                self.logger.warning(f"Failed to initialize RAG handler: {e}")
        
        # Determine starting step
        start_index = 0
        if resume_from:
            try:
                start_index = self.step_order.index(resume_from)
            except ValueError:
                self.logger.error(f"Invalid resume step: {resume_from}")
                start_index = 0
        
        # Execute pipeline steps
        self.current_state.status = PipelineStatus.IN_PROGRESS
        
        try:
            for step in self.step_order[start_index:]:
                self.logger.info(f"Executing step: {step.value}")
                self.current_state.current_step = step
                
                # Execute step with retry logic
                step_result = await self._execute_step_with_retry(
                    step, 
                    documentation,
                    self.current_state.step_results
                )
                
                # Store result
                self.current_state.step_results[step] = step_result
                
                # Update metrics
                if step_result.generation_result:
                    self.current_state.total_cost += step_result.generation_result.cost
                    self.current_state.total_tokens += step_result.generation_result.total_tokens
                
                # Check if pipeline should halt
                if step_result.status == PipelineStatus.FAILED:
                    self.logger.error(f"Step {step.value} failed: {step_result.error}")
                    if self._should_halt_on_failure(step, step_result):
                        self.current_state.status = PipelineStatus.HALTED
                        break
                
                # Save state after each step
                self._save_pipeline_state()
                
                # Log progress
                self._log_progress()
            
            # Set final status
            if self.current_state.status == PipelineStatus.IN_PROGRESS:
                self.current_state.status = PipelineStatus.COMPLETED
            
        except Exception as e:
            self.logger.error(f"Pipeline error: {e}")
            self.current_state.status = PipelineStatus.FAILED
            self.current_state.metadata["error"] = str(e)
            self.current_state.metadata["traceback"] = traceback.format_exc()
        
        finally:
            self.current_state.end_time = datetime.now()
            self._save_pipeline_state()
            
            # Cleanup
            if self.rag_handler:
                self.rag_handler.disconnect()
        
        return self.current_state
    
    async def _execute_step_with_retry(
        self,
        step: PipelineStep,
        documentation: str,
        previous_results: Dict[PipelineStep, StepResult]
    ) -> StepResult:
        """Execute a pipeline step with retry logic."""
        retry_config = self.config.get("pipeline", {}).get("retry", {})
        max_attempts = retry_config.get("max_attempts", 3)
        backoff_multiplier = retry_config.get("backoff_multiplier", 2)
        initial_delay = retry_config.get("initial_delay", 5)
        
        last_error = None
        
        for attempt in range(max_attempts):
            try:
                # Execute step
                result = await self._execute_step(step, documentation, previous_results)
                result.retry_count = attempt
                
                # Validate result
                if result.validation_result and not result.validation_result.valid:
                    # Check if we should retry on validation failure
                    if attempt < max_attempts - 1 and self._should_retry_on_validation_failure(result):
                        self.logger.warning(f"Validation failed for {step.value}, retrying...")
                        await asyncio.sleep(initial_delay * (backoff_multiplier ** attempt))
                        continue
                
                return result
                
            except Exception as e:
                last_error = e
                self.logger.error(f"Error in step {step.value} (attempt {attempt + 1}): {e}")
                
                if attempt < max_attempts - 1:
                    await asyncio.sleep(initial_delay * (backoff_multiplier ** attempt))
                    
                    # Try with fallback model
                    self.logger.info(f"Attempting with fallback model for {step.value}")
        
        # All attempts failed
        return StepResult(
            step=step,
            status=PipelineStatus.FAILED,
            data=None,
            error=str(last_error),
            retry_count=max_attempts
        )
    
    async def _execute_step(
        self,
        step: PipelineStep,
        documentation: str,
        previous_results: Dict[PipelineStep, StepResult]
    ) -> StepResult:
        """Execute a single pipeline step."""
        start_time = time.time()
        
        # Get step-specific method
        step_methods = {
            PipelineStep.SECTION_SUMMARY: self._step1_section_summary,
            PipelineStep.DATA_EXTRACTION: self._step2_data_extraction,
            PipelineStep.REGISTER_MAPPING: self._step3_register_mapping,
            PipelineStep.ARCHITECTURE_PLANNING: self._step4_architecture_planning,
            PipelineStep.TODO_GENERATION: self._step5_todo_generation,
            PipelineStep.CODE_GENERATION: self._step6_code_generation
        }
        
        method = step_methods.get(step)
        if not method:
            raise ValueError(f"Unknown step: {step}")
        
        # Execute step
        result = await method(documentation, previous_results)
        
        # Add execution time
        result.metadata = result.metadata or {}
        result.metadata["execution_time"] = time.time() - start_time
        
        return result
    
    async def _step1_section_summary(
        self,
        documentation: str,
        previous_results: Dict[PipelineStep, StepResult]
    ) -> StepResult:
        """Step 1: Generate section summaries from documentation."""
        self.logger.info("Step 1: Generating section summaries")
        
        # Build prompt with few-shot examples
        prompt = self._build_section_summary_prompt(documentation)
        
        # Generate with appropriate model
        generation_result = self.model_manager.generate(
            prompt=prompt,
            step_name="analysis",
            temperature=0.3,
            response_format="json",
            validation_schema={
                "type": "object",
                "properties": {
                    "overview": {"type": "string"},
                    "registers": {"type": "string"},
                    "functionality": {"type": "string"},
                    "interrupts": {"type": "string"},
                    "timing": {"type": "string"},
                    "key_features": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["overview", "registers", "functionality"]
            }
        )
        
        # Parse response
        try:
            summary_data = json.loads(generation_result.content)
        except json.JSONDecodeError:
            summary_data = {"error": "Failed to parse JSON response"}
        
        # Validate
        validation_result = self.validation_engine.validate_step("section_summary", summary_data)
        
        return StepResult(
            step=PipelineStep.SECTION_SUMMARY,
            status=PipelineStatus.COMPLETED if validation_result.valid else PipelineStatus.FAILED,
            data=summary_data,
            validation_result=validation_result,
            generation_result=generation_result
        )
    
    async def _step2_data_extraction(
        self,
        documentation: str,
        previous_results: Dict[PipelineStep, StepResult]
    ) -> StepResult:
        """Step 2: Extract high-level peripheral metadata."""
        self.logger.info("Step 2: Extracting peripheral metadata")
        
        # Get previous summary
        summary = previous_results[PipelineStep.SECTION_SUMMARY].data
        
        # Build prompt
        prompt = self._build_data_extraction_prompt(documentation, summary)
        
        # Generate
        generation_result = self.model_manager.generate(
            prompt=prompt,
            step_name="analysis",
            temperature=0.2,
            response_format="json",
            validation_schema={
                "type": "object",
                "properties": {
                    "peripheral_name": {"type": "string"},
                    "base_address": {"type": "string"},
                    "size": {"type": "integer"},
                    "interrupts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "number": {"type": "integer"},
                                "description": {"type": "string"}
                            },
                            "required": ["name", "number"]
                        }
                    },
                    "clock_domains": {"type": "array", "items": {"type": "string"}},
                    "interfaces": {"type": "array", "items": {"type": "string"}},
                    "dma_channels": {"type": "integer"},
                    "features": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["peripheral_name", "base_address"]
            }
        )
        
        # Parse response
        try:
            metadata = json.loads(generation_result.content)
        except json.JSONDecodeError:
            metadata = {"error": "Failed to parse JSON response"}
        
        # Validate
        validation_result = self.validation_engine.validate_step("data_extraction", metadata)
        
        return StepResult(
            step=PipelineStep.DATA_EXTRACTION,
            status=PipelineStatus.COMPLETED if validation_result.valid else PipelineStatus.FAILED,
            data=metadata,
            validation_result=validation_result,
            generation_result=generation_result
        )
    
    async def _step3_register_mapping(
        self,
        documentation: str,
        previous_results: Dict[PipelineStep, StepResult]
    ) -> StepResult:
        """Step 3: Detailed register and bit-field mapping (MOST CRITICAL)."""
        self.logger.info("Step 3: Mapping registers and bit-fields (CRITICAL)")
        
        # Get previous results
        summary = previous_results[PipelineStep.SECTION_SUMMARY].data
        metadata = previous_results[PipelineStep.DATA_EXTRACTION].data
        
        # Multi-pass approach for accuracy
        max_passes = 3
        best_result = None
        best_score = 0.0
        
        for pass_num in range(max_passes):
            self.logger.info(f"Register mapping pass {pass_num + 1}/{max_passes}")
            
            # Build prompt with increasing detail
            prompt = self._build_register_mapping_prompt(
                documentation, 
                summary, 
                metadata,
                pass_num=pass_num,
                previous_attempt=best_result.data if best_result else None
            )
            
            # Use best model for this critical step
            generation_result = self.model_manager.generate(
                prompt=prompt,
                model=self.model_manager.get_best_model_for_task(
                    "analysis",
                    {"json_support": True, "min_tokens": 4096}
                ),
                temperature=0.1,  # Low temperature for accuracy
                response_format="json",
                validation_schema={
                    "type": "object",
                    "properties": {
                        "registers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "address": {"type": "string"},
                                    "size": {"type": "integer"},
                                    "access": {"type": "string"},
                                    "reset_value": {"type": "string"},
                                    "description": {"type": "string"},
                                    "bit_fields": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"},
                                                "start_bit": {"type": "integer"},
                                                "end_bit": {"type": "integer"},
                                                "access": {"type": "string"},
                                                "description": {"type": "string"},
                                                "values": {"type": "object"}
                                            },
                                            "required": ["name", "start_bit", "end_bit"]
                                        }
                                    }
                                },
                                "required": ["name", "address", "size", "access"]
                            }
                        }
                    },
                    "required": ["registers"]
                }
            )
            
            # Parse response
            try:
                register_data = json.loads(generation_result.content)
            except json.JSONDecodeError:
                continue
            
            # Validate with extra scrutiny
            validation_result = self.validation_engine.validate_step("register_mapping", register_data)
            
            # Check if this is the best result so far
            if validation_result.score > best_score:
                best_score = validation_result.score
                best_result = StepResult(
                    step=PipelineStep.REGISTER_MAPPING,
                    status=PipelineStatus.COMPLETED if validation_result.valid else PipelineStatus.FAILED,
                    data=register_data,
                    validation_result=validation_result,
                    generation_result=generation_result
                )
            
            # Stop if we have a perfect score
            if validation_result.score >= 95.0:
                break
        
        # Log final score
        self.logger.info(f"Register mapping completed with score: {best_score}")
        
        # Human intervention for critical failures
        if best_score < 70.0 and self.human_intervention_enabled:
            best_result = await self._request_human_intervention(
                PipelineStep.REGISTER_MAPPING,
                best_result,
                "Register mapping score below threshold"
            )
        
        return best_result
    
    async def _step4_architecture_planning(
        self,
        documentation: str,
        previous_results: Dict[PipelineStep, StepResult]
    ) -> StepResult:
        """Step 4: Plan Renode peripheral architecture."""
        self.logger.info("Step 4: Planning peripheral architecture")
        
        # Get previous results
        metadata = previous_results[PipelineStep.DATA_EXTRACTION].data
        registers = previous_results[PipelineStep.REGISTER_MAPPING].data
        
        # Build prompt
        prompt = self._build_architecture_prompt(metadata, registers)
        
        # Generate
        generation_result = self.model_manager.generate(
            prompt=prompt,
            step_name="code_generation",
            temperature=0.4,
            response_format="json",
            validation_schema={
                "type": "object",
                "properties": {
                    "class_structure": {
                        "type": "object",
                        "properties": {
                            "class_name": {"type": "string"},
                            "base_class": {"type": "string"},
                            "interfaces": {"type": "array", "items": {"type": "string"}},
                            "namespaces": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["class_name", "base_class"]
                    },
                    "interfaces": {"type": "array", "items": {"type": "string"}},
                    "dependencies": {"type": "array", "items": {"type": "string"}},
                    "design_patterns": {"type": "array", "items": {"type": "string"}},
                    "register_groups": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "registers": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    }
                },
                "required": ["class_structure", "interfaces", "dependencies"]
            }
        )
        
        # Parse response
        try:
            architecture = json.loads(generation_result.content)
        except json.JSONDecodeError:
            architecture = {"error": "Failed to parse JSON response"}
        
        # Validate
        validation_result = self.validation_engine.validate_step("architecture", architecture)
        
        return StepResult(
            step=PipelineStep.ARCHITECTURE_PLANNING,
            status=PipelineStatus.COMPLETED if validation_result.valid else PipelineStatus.FAILED,
            data=architecture,
            validation_result=validation_result,
            generation_result=generation_result
        )
    
    async def _step5_todo_generation(
        self,
        documentation: str,
        previous_results: Dict[PipelineStep, StepResult]
    ) -> StepResult:
        """Step 5: Generate detailed implementation todo list."""
        self.logger.info("Step 5: Generating implementation todo list")
        
        # Get context from previous steps
        summary = previous_results[PipelineStep.SECTION_SUMMARY].data
        metadata = previous_results[PipelineStep.DATA_EXTRACTION].data
        registers = previous_results[PipelineStep.REGISTER_MAPPING].data
        architecture = previous_results[PipelineStep.ARCHITECTURE_PLANNING].data
        
        # Use TodoProcessor for structured generation
        peripheral_name = metadata.get("peripheral_name", "Unknown")
        context_summary = json.dumps({
            "summary": summary,
            "metadata": metadata,
            "architecture": architecture
        }, indent=2)
        
        # Generate todo list
        todo_list = self.todo_processor.generate_todo_list(
            peripheral_name=peripheral_name,
            context_summary=context_summary,
            documentation=documentation
        )
        
        # Generate chain-of-thought reasoning
        cot_analysis = self.todo_processor.generate_chain_of_thought(
            todo_list=todo_list,
            peripheral_name=peripheral_name
        )
        
        # Enhance with LLM for granular tasks
        enhanced_prompt = self._build_todo_enhancement_prompt(
            todo_list, 
            registers, 
            architecture
        )
        
        generation_result = self.model_manager.generate(
            prompt=enhanced_prompt,
            step_name="analysis",
            temperature=0.5,
            response_format="json"
        )
        
        # Parse enhanced todos
        try:
            enhanced_data = json.loads(generation_result.content)
            final_todos = {
                "todos": enhanced_data.get("enhanced_todos", todo_list),
                "chain_of_thought": cot_analysis,
                "implementation_order": enhanced_data.get("implementation_order", [])
            }
        except json.JSONDecodeError:
            final_todos = {
                "todos": todo_list,
                "chain_of_thought": cot_analysis,
                "implementation_order": []
            }
        
        # Validate
        validation_result = self.validation_engine.validate_step("todo_list", final_todos)
        
        return StepResult(
            step=PipelineStep.TODO_GENERATION,
            status=PipelineStatus.COMPLETED if validation_result.valid else PipelineStatus.FAILED,
            data=final_todos,
            validation_result=validation_result,
            generation_result=generation_result
        )
    
    async def _step6_code_generation(
        self,
        documentation: str,
        previous_results: Dict[PipelineStep, StepResult]
    ) -> StepResult:
        """Step 6: Generate C# code following todo list."""
        self.logger.info("Step 6: Generating C# implementation")
        
        # Get all previous results
        metadata = previous_results[PipelineStep.DATA_EXTRACTION].data
        registers = previous_results[PipelineStep.REGISTER_MAPPING].data
        architecture = previous_results[PipelineStep.ARCHITECTURE_PLANNING].data
        todos = previous_results[PipelineStep.TODO_GENERATION].data
        
        # Section-by-section generation
        code_sections = []
        
        # 1. Generate file header and usings
        header_prompt = self._build_code_header_prompt(metadata, architecture)
        header_result = self.model_manager.generate(
            prompt=header_prompt,
            step_name="code_generation",
            temperature=0.1
        )
        code_sections.append(("header", header_result.content))
        
        # 2. Generate class definition and constructor
        class_prompt = self._build_class_definition_prompt(metadata, architecture)
        class_result = self.model_manager.generate(
            prompt=class_prompt,
            step_name="code_generation",
            temperature=0.1
        )
        code_sections.append(("class_definition", class_result.content))
        
        # 3. Generate register definitions
        register_prompt = self._build_register_definitions_prompt(registers)
        register_result = self.model_manager.generate(
            prompt=register_prompt,
            step_name="code_generation",
            temperature=0.1,
            max_tokens=8192
        )
        code_sections.append(("registers", register_result.content))
        
        # 4. Generate method implementations based on todos
        high_priority_todos = [t for t in todos["todos"] if t.get("priority") in [1, 2]]
        for todo in high_priority_todos[:5]:  # Limit to top 5 for initial implementation
            if todo.get("category") == "implementation":
                method_prompt = self._build_method_implementation_prompt(todo, registers)
                method_result = self.model_manager.generate(
                    prompt=method_prompt,
                    step_name="code_generation",
                    temperature=0.2
                )
                code_sections.append((f"method_{todo['id']}", method_result.content))
        
        # 5. Assemble final code
        final_code = self._assemble_code_sections(code_sections)# Calculate total generation cost
        total_cost = sum(
            section_result.cost if hasattr(section_result, 'cost') else 0
            for _, section_result in [(k, v) for k, v in locals().items() if k.endswith('_result')]
        )
        
        # Create final result
        code_data = {
            "code": final_code,
            "sections": {name: content for name, content in code_sections},
            "peripheral_name": metadata.get("peripheral_name", "UnknownPeripheral"),
            "file_name": f"{metadata.get('peripheral_name', 'UnknownPeripheral')}.cs"
        }
        
        # Validate generated code
        validation_result = self.validation_engine.validate_step("code_generation", code_data)
        
        # Create aggregated generation result
        generation_result = GenerationResult(
            content=final_code,
            model="multi-model",
            provider=self.model_manager.models[list(self.model_manager.models.keys())[0]].provider,
            prompt_tokens=0,
            response_tokens=len(final_code.split()),
            total_tokens=len(final_code.split()),
            response_time=0.0,
            cost=total_cost,
            confidence_score=validation_result.score / 100.0,
            validation_passed=validation_result.valid,
            retry_count=0
        )
        
        return StepResult(
            step=PipelineStep.CODE_GENERATION,
            status=PipelineStatus.COMPLETED if validation_result.valid else PipelineStatus.FAILED,
            data=code_data,
            validation_result=validation_result,
            generation_result=generation_result
        )
    
    def _build_section_summary_prompt(self, documentation: str) -> str:
        """Build prompt for section summarization."""
        return f"""You are an expert at analyzing technical documentation for hardware peripherals.
Your task is to create a structured summary of the peripheral documentation.

DOCUMENTATION:
{documentation[:8000]}  # Limit to prevent token overflow

Please analyze this documentation and provide a JSON summary with the following structure:
{{
    "overview": "High-level description of the peripheral and its purpose",
    "registers": "Summary of register organization and key registers",
    "functionality": "Core functionality and operating modes",
    "interrupts": "Interrupt sources and handling (if applicable)",
    "timing": "Timing requirements and constraints",
    "key_features": ["List", "of", "key", "features"]
}}

Focus on extracting information that will be essential for implementing a Renode model.
Be thorough but concise. Ensure all JSON is properly formatted.

EXAMPLE OUTPUT:
{{
    "overview": "The UART peripheral provides asynchronous serial communication with configurable baud rate, data bits, parity, and stop bits.",
    "registers": "The peripheral has 8 registers starting at base address. Key registers include Control Register (CTRL), Status Register (STAT), and Data Register (DATA).",
    "functionality": "Supports full-duplex communication, hardware flow control, and DMA transfers. Operating modes include normal UART, IrDA, and RS-485.",
    "interrupts": "Generates interrupts for TX empty, RX full, and various error conditions",
    "timing": "Baud rate generator supports rates from 110 to 921600 bps with <2% error",
    "key_features": ["Full duplex operation", "Hardware flow control", "DMA support", "FIFO buffers", "Multi-processor communication"]
}}"""
    
    def _build_data_extraction_prompt(self, documentation: str, summary: Dict[str, Any]) -> str:
        """Build prompt for data extraction."""
        return f"""Based on the peripheral documentation and summary, extract detailed metadata.

SUMMARY:
{json.dumps(summary, indent=2)}

DOCUMENTATION EXCERPT:
{documentation[:6000]}

Extract and provide the following peripheral metadata in JSON format:
{{
    "peripheral_name": "PeripheralName",
    "base_address": "0x40000000",  // Hex format
    "size": 4096,  // Address space size in bytes
    "interrupts": [
        {{"name": "UART_IRQ", "number": 37, "description": "UART interrupt"}}
    ],
    "clock_domains": ["PCLK", "UART_CLK"],
    "interfaces": ["UART", "DMA"],  // Communication interfaces
    "dma_channels": 2,  // Number of DMA channels if applicable
    "features": ["Feature1", "Feature2"]  // Key features list
}}

Be precise with addresses and interrupt numbers. If information is not available, use reasonable defaults or omit the field.

EXAMPLE for a Timer peripheral:
{{
    "peripheral_name": "Timer32",
    "base_address": "0x40001000",
    "size": 256,
    "interrupts": [
        {{"name": "TIMER_IRQ", "number": 15, "description": "Timer overflow interrupt"}}
    ],
    "clock_domains": ["PCLK"],
    "interfaces": ["APB"],
    "dma_channels": 0,
    "features": ["32-bit counter", "Prescaler", "Compare match", "PWM generation"]
}}"""
    
    def _build_register_mapping_prompt(
        self, 
        documentation: str, 
        summary: Dict[str, Any],
        metadata: Dict[str, Any],
        pass_num: int = 0,
        previous_attempt: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build prompt for register mapping (with multi-pass refinement)."""
        base_prompt = f"""You are an expert at extracting register definitions from hardware documentation.
This is a CRITICAL step that requires extreme accuracy.

PERIPHERAL: {metadata.get('peripheral_name', 'Unknown')}
BASE ADDRESS: {metadata.get('base_address', '0x0')}

DOCUMENTATION:
{documentation[:10000]}

"""
        
        if pass_num == 0:
            base_prompt += """Extract ALL registers with complete details. For each register provide:
- name: Exact register name from documentation
- address: Offset from base address (hex format like "0x00")
- size: Register size in bits (8, 16, or 32)
- access: Access type (RO, WO, RW, W1C, W1S, RC)
- reset_value: Reset value in hex
- description: Register purpose
- bit_fields: Array of ALL bit fields with:
  - name: Field name
  - start_bit: Starting bit position (0-based)
  - end_bit: Ending bit position (inclusive)
  - access: Field access type
  - description: Field purpose
  - values: Object mapping values to meanings (if applicable)

CRITICAL RULES:
1. Include EVERY register mentioned in the documentation
2. Bit positions must be exact and not overlap
3. All addresses must be unique
4. Access permissions must match documentation exactly

EXAMPLE OUTPUT:"""
        
        elif pass_num == 1 and previous_attempt:
            base_prompt += f"""PREVIOUS ATTEMPT:
{json.dumps(previous_attempt, indent=2)}

Please REFINE the register definitions by:
1. Double-checking all bit field positions
2. Ensuring no registers are missing
3. Verifying all addresses are correct
4. Adding any missing reset values
5. Correcting any access permission errors

Focus on accuracy over completeness. Fix any errors from the previous attempt."""
        
        else:  # pass_num >= 2
            base_prompt += """This is the FINAL verification pass. 
Ensure ABSOLUTE accuracy for:
1. Every bit field start/end position
2. Register addresses (no conflicts)
3. Access permissions
4. Reset values

If you're unsure about any detail, mark it with a comment in the description."""
        
        base_prompt += """

{
    "registers": [
        {
            "name": "CTRL",
            "address": "0x00",
            "size": 32,
            "access": "RW",
            "reset_value": "0x00000000",
            "description": "Control Register",
            "bit_fields": [
                {
                    "name": "ENABLE",
                    "start_bit": 0,
                    "end_bit": 0,
                    "access": "RW",
                    "description": "Enable peripheral",
                    "values": {"0": "Disabled", "1": "Enabled"}
                },
                {
                    "name": "MODE",
                    "start_bit": 1,
                    "end_bit": 2,
                    "access": "RW",
                    "description": "Operating mode",
                    "values": {"0": "Mode0", "1": "Mode1", "2": "Mode2", "3": "Mode3"}
                }
            ]
        }
    ]
}"""
        
        return base_prompt
    
    def _build_architecture_prompt(self, metadata: Dict[str, Any], registers: Dict[str, Any]) -> str:
        """Build prompt for architecture planning."""
        return f"""Design the C# class architecture for a Renode peripheral model.

PERIPHERAL INFO:
{json.dumps(metadata, indent=2)}

REGISTER COUNT: {len(registers.get('registers', []))}
INTERFACES: {', '.join(metadata.get('interfaces', []))}

Design a clean architecture following Renode patterns:

{{
    "class_structure": {{
        "class_name": "PeripheralNamePeripheral",
        "base_class": "IDoubleWordPeripheral",  // or IWordPeripheral, IBytePeripheral
        "interfaces": ["IKnownSize"],  // Additional interfaces
        "namespaces": ["Antmicro.Renode.Peripherals.SpecificType"]
    }},
    "interfaces": ["IDoubleWordPeripheral", "IKnownSize"],  // All implemented interfaces
    "dependencies": [
        "Antmicro.Renode.Core",
        "Antmicro.Renode.Peripherals.Bus"
    ],
    "design_patterns": ["RegistersCollection", "FieldDefinition"],
    "register_groups": [
        {{
            "name": "ControlRegisters",
            "registers": ["CTRL", "STATUS"]
        }}
    ]
}}

Follow these Renode conventions:
1. Use appropriate peripheral interface based on register size
2. Include IKnownSize for memory-mapped peripherals  
3. Group related registers logically
4. Use Renode's RegistersCollection pattern
5. Plan for proper reset handling

EXAMPLE for UART:
{{
    "class_structure": {{
        "class_name": "UARTPeripheral",
        "base_class": "IDoubleWordPeripheral",
        "interfaces": ["IKnownSize", "IUART"],
        "namespaces": ["Antmicro.Renode.Peripherals.UART"]
    }},
    "interfaces": ["IDoubleWordPeripheral", "IKnownSize", "IUART"],
    "dependencies": [
        "Antmicro.Renode.Core",
        "Antmicro.Renode.Peripherals.Bus",
        "Antmicro.Renode.Peripherals.UART"
    ],
    "design_patterns": ["RegistersCollection", "DoubleWordRegister", "FlagRegisterField"],
    "register_groups": [
        {{
            "name": "ControlRegisters",
            "registers": ["CTRL", "BAUD"]
        }},
        {{
            "name": "StatusRegisters", 
            "registers": ["STATUS", "FLAGS"]
        }},
        {{
            "name": "DataRegisters",
            "registers": ["DATA", "FIFO"]
        }}
    ]
}}"""
    
    def _build_todo_enhancement_prompt(
        self,
        todo_list: List[Dict[str, Any]],
        registers: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> str:
        """Build prompt to enhance todo list with granular tasks."""
        return f"""Enhance the implementation todo list with more granular, actionable tasks.

CURRENT TODO LIST:
{json.dumps(todo_list[:10], indent=2)}  # First 10 tasks

REGISTER COUNT: {len(registers.get('registers', []))}
ARCHITECTURE: {architecture.get('class_structure', {}).get('class_name', 'Unknown')}

Enhance the todo list by:
1. Breaking down high-level tasks into specific implementation steps
2. Adding register-specific implementation tasks
3. Including Renode-specific patterns and requirements
4. Providing a logical implementation order

Return JSON with:
{{
    "enhanced_todos": [
        {{
            "id": "task_0001",
            "title": "Specific actionable task",
            "description": "Detailed description with Renode context",
            "category": "implementation",
            "priority": 1,  // 1=CRITICAL, 2=HIGH, 3=MEDIUM, 4=LOW
            "estimated_hours": 2.5,
            "dependencies": ["task_0000"],
            "renode_pattern": "RegistersCollection"  // Relevant Renode pattern
        }}
    ],
    "implementation_order": ["task_0001", "task_0002", "..."]
}}

Focus on creating tasks that a developer can immediately act upon.
Each task should be completable in 1-4 hours."""
    
    def _build_code_header_prompt(self, metadata: Dict[str, Any], architecture: Dict[str, Any]) -> str:
        """Build prompt for code header generation."""
        return f"""Generate the C# file header and using statements for a Renode peripheral.

PERIPHERAL: {metadata.get('peripheral_name', 'Unknown')}
NAMESPACE: {'.'.join(architecture.get('class_structure', {}).get('namespaces', ['Antmicro.Renode.Peripherals']))}
INTERFACES: {', '.join(architecture.get('interfaces', []))}

Generate:
1. File header comment with description
2. Copyright notice (use Antmicro standard)
3. All required using statements
4. Namespace declaration

Follow Renode coding standards exactly.

EXAMPLE OUTPUT:
//
// Copyright (c) 2024 Antmicro
//
// This file is licensed under the MIT License.
// Full license text is available in 'licenses/MIT.txt'.
//
// Description: Timer32 - 32-bit timer peripheral with compare and PWM functionality
//

using System;
using System.Collections.Generic;
using Antmicro.Renode.Core;
using Antmicro.Renode.Core.Structure.Registers;
using Antmicro.Renode.Logging;
using Antmicro.Renode.Peripherals.Bus;
using Antmicro.Renode.Peripherals.Timers;

namespace Antmicro.Renode.Peripherals.Timers
{{"""
    
    def _build_class_definition_prompt(self, metadata: Dict[str, Any], architecture: Dict[str, Any]) -> str:
        """Build prompt for class definition and constructor."""
        class_info = architecture.get('class_structure', {})
        return f"""Generate the C# class definition and constructor for the Renode peripheral.

CLASS NAME: {class_info.get('class_name', 'UnknownPeripheral')}
BASE CLASS: {class_info.get('base_class', 'IDoubleWordPeripheral')}
INTERFACES: {', '.join(architecture.get('interfaces', []))}
PERIPHERAL TYPE: {metadata.get('peripheral_name', 'Unknown')}

Generate:
1. Class declaration with proper inheritance
2. Private fields for registers collection and state
3. Constructor with Machine parameter
4. IKnownSize implementation if needed
5. Basic initialization

Follow Renode patterns:
- Use RegistersCollection for register management
- Initialize logging with peripheral name
- Set up reset handler
- Define register collection in constructor

EXAMPLE OUTPUT:
public class Timer32Peripheral : BasicDoubleWordPeripheral, IKnownSize, ITimer
{{
    public Timer32Peripheral(Machine machine) : base(machine)
    {{
        var registersMap = new Dictionary<long, DoubleWordRegister>
        {{
            {{(long)Registers.Control, new DoubleWordRegister(this)
                .WithFlag(0, out enableFlag, name: "ENABLE")
                .WithValueField(1, 2, out modeField, name: "MODE")
            }},
            {{(long)Registers.Status, new DoubleWordRegister(this)
                .WithFlag(0, FieldMode.Read, valueProviderCallback: _ => isRunning, name: "RUNNING")
                .WithFlag(1, FieldMode.Read | FieldMode.WriteOneToClear, name: "OVERFLOW")
            }}
        }};

        registers = new DoubleWordRegisterCollection(this, registersMap);
        Reset();
    }}

    public long Size => 0x100;

    public override void Reset()
    {{
        base.Reset();
        isRunning = false;
        currentValue = 0;
    }}

    private readonly DoubleWordRegisterCollection registers;
    private readonly IFlagRegisterField enableFlag;
    private readonly IValueRegisterField modeField;
    private bool isRunning;
    private uint currentValue;"""
    
    def _build_register_definitions_prompt(self, registers: Dict[str, Any]) -> str:
        """Build prompt for register definitions."""
        reg_list = registers.get('registers', [])
        return f"""Generate Renode RegistersCollection definitions for all peripheral registers.

REGISTERS TO IMPLEMENT ({len(reg_list)} total):
{json.dumps(reg_list[:5], indent=2)}  # Show first 5 as examples

For each register, create a DoubleWordRegister with:
1. Proper bit field definitions using WithFlag/WithValueField
2. Correct access modes (Read, Write, WriteOneToClear, etc.)
3. Meaningful field names
4. Reset values
5. Callbacks where needed

Use these Renode patterns:
- WithFlag for single bits
- WithValueField for multi-bit fields
- WithReservedBits for unused bits
- FieldMode.Read/Write/WriteOneToClear as appropriate
- changeCallback/valueProviderCallback for dynamic behavior

EXAMPLE for a control register with multiple fields:
{{(long)Registers.Control, new DoubleWordRegister(this, 0x00000000)
    .WithFlag(0, out enableFlag, name: "ENABLE")
    .WithValueField(1, 3, out modeField, name: "MODE", 
        changeCallback: (_, value) => UpdateMode((uint)value))
    .WithFlag(4, out interruptEnableFlag, name: "IE")
    .WithReservedBits(5, 3)
    .WithValueField(8, 8, out prescalerField, name: "PRESCALER")
    .WithReservedBits(16, 16)
}},

Generate definitions for ALL registers following this pattern."""
    
    def _build_method_implementation_prompt(self, todo: Dict[str, Any], registers: Dict[str, Any]) -> str:
        """Build prompt for method implementation based on todo."""
        return f"""Implement the following method for the Renode peripheral:

TASK: {todo.get('title', 'Unknown task')}
DESCRIPTION: {todo.get('description', '')}
CATEGORY: {todo.get('category', 'implementation')}

AVAILABLE REGISTERS: {len(registers.get('registers', []))}

Generate a complete C# method implementation that:
1. Follows Renode coding patterns
2. Includes proper error handling
3. Uses appropriate logging
4. Handles edge cases
5. Is well-commented

If this is a register read/write handler, implement ReadDoubleWord/WriteDoubleWord.
If this is a functional method, implement with proper state management.

EXAMPLE for a timer start method:
private void StartTimer()
{{
    if (!enableFlag.Value)
    {{
        this.Log(LogLevel.Warning, "Attempted to start timer while disabled");
        return;
    }}

    isRunning = true;
    lastUpdateTime = machine.ClockSource.CurrentValue;
    
    this.Log(LogLevel.Debug, "Timer started in mode {{0}}", modeField.Value);
    
    UpdateInterrupts();
}}"""
    
    def _assemble_code_sections(self, sections: List[Tuple[str, str]]) -> str:
        """Assemble code sections into final C# file."""
        # Start with header
        final_code = ""
        
        # Add sections in order
        for section_name, content in sections:
            if section_name == "header":
                final_code += content + "\n"
            elif section_name == "class_definition":
                # Ensure we're inside namespace
                if not final_code.strip().endswith("{"):
                    final_code += "{\n"
                final_code += "\n" + content
            elif section_name == "registers":
                # Insert register definitions in constructor
                # This is a simplified approach - in production would parse and merge properly
                final_code += "\n\n    // Register Definitions\n" + content
            else:
                # Add methods
                final_code += "\n\n" + content
        
        # Close class and namespace
        if not final_code.rstrip().endswith("}"):
            final_code += "\n    }\n}"
        
        return final_code
    
    def _should_halt_on_failure(self, step: PipelineStep, result: StepResult) -> bool:
        """Determine if pipeline should halt on step failure."""
        # Always halt on critical steps
        critical_steps = [
            PipelineStep.REGISTER_MAPPING,
            PipelineStep.CODE_GENERATION
        ]
        
        if step in critical_steps:
            return True
        
        # Check validation score
        if result.validation_result:
            min_score = self.config.get("validation", {}).get("min_validation_score", 70.0)
            if result.validation_result.score < min_score:
                return True
        
        # Check for critical errors
        if result.validation_result:
            critical_errors = [
                issue for issue in result.validation_result.issues
                if issue.severity == Severity.ERROR
            ]
            if len(critical_errors) > 3:
                return True
        
        return False
    
    def _should_retry_on_validation_failure(self, result: StepResult) -> bool:
        """Determine if step should be retried on validation failure."""
        if not result.validation_result:
            return False
        
        # Retry if score is close to passing
        score = result.validation_result.score
        min_score = self.config.get("validation", {}).get("min_validation_score", 70.0)
        
        if score >= min_score * 0.8:  # Within 80% of passing
            return True
        
        # Retry if only minor issues
        error_count = sum(
            1 for issue in result.validation_result.issues
            if issue.severity == Severity.ERROR
        )
        
        return error_count <= 2
    
    async def _request_human_intervention(
        self,
        step: PipelineStep,
        result: StepResult,
        reason: str
    ) -> StepResult:
        """Request human intervention for critical issues."""
        self.logger.warning(f"Human intervention requested for {step.value}: {reason}")
        
        # In a real implementation, this would:
        # 1. Send notification to human reviewer
        # 2. Provide interface for corrections
        # 3. Wait for human input
        # 4. Validate corrections
        
        # For now, just log and return original result
        result.metadata = result.metadata or {}
        result.metadata["human_intervention_requested"] = True
        result.metadata["intervention_reason"] = reason
        
        return result
    
    def _generate_pipeline_id(self) -> str:
        """Generate unique pipeline ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"pipeline_{timestamp}"
    
    def _load_documentation(self, doc_path: str) -> Optional[str]:
        """Load documentation from file."""
        try:
            path = Path(doc_path)
            if not path.exists():
                self.logger.error(f"Documentation file not found: {doc_path}")
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"Error loading documentation: {e}")
            return None
    
    def _save_pipeline_state(self) -> None:
        """Save current pipeline state to disk."""
        if not self.current_state:
            return
        
        state_dir = Path("pipeline_states")
        state_dir.mkdir(exist_ok=True)
        
        state_file = state_dir / f"{self.current_state.pipeline_id}.json"
        
        try:
            with open(state_file, 'w') as f:
                json.dump(self.current_state.to_dict(), f, indent=2)
            self.logger.debug(f"Saved pipeline state to {state_file}")
        except Exception as e:
            self.logger.error(f"Error saving pipeline state: {e}")
    
    def _load_pipeline_state(self, pipeline_id: str) -> Optional[PipelineState]:
        """Load pipeline state from disk."""
        state_file = Path("pipeline_states") / f"{pipeline_id}.json"
        
        if not state_file.exists():
            self.logger.error(f"Pipeline state not found: {pipeline_id}")
            return None
        
        try:
            with open(state_file, 'r') as f:
                data = json.load(f)
            return PipelineState.from_dict(data)
        except Exception as e:
            self.logger.error(f"Error loading pipeline state: {e}")
            return None
    
    def _log_progress(self) -> None:
        """Log pipeline progress and ETA."""
        if not self.current_state:
            return
        
        completed_steps = len(self.current_state.step_results)
        total_steps = len(self.step_order)
        progress = (completed_steps / total_steps) * 100
        
        self.logger.info(f"Pipeline progress: {progress:.1f}% ({completed_steps}/{total_steps} steps)")
        
        # Estimate time remaining
        if self.current_state.start_time and completed_steps > 0:
            elapsed = datetime.now() - self.current_state.start_time
            avg_time_per_step = elapsed / completed_steps
            remaining_steps = total_steps - completed_steps
            eta = datetime.now() + (avg_time_per_step * remaining_steps)
            self.logger.info(f"Estimated completion: {eta.strftime('%H:%M:%S')}")
    
    def get_pipeline_metrics(self) -> Dict[str, Any]:
        """Get comprehensive pipeline metrics."""
        if not self.current_state:
            return {}
        
        metrics = {
            "pipeline_id": self.current_state.pipeline_id,
            "peripheral_name": self.current_state.peripheral_name,
            "status": self.current_state.status.value,
            "total_cost": self.current_state.total_cost,
            "total_tokens": self.current_state.total_tokens,
            "steps_completed": len(self.current_state.step_results),
            "steps_total": len(self.step_order),
            "step_metrics": {}
        }
        
        # Add per-step metrics
        for step, result in self.current_state.step_results.items():
            step_metric = {
                "status": result.status.value,
                "validation_score": result.validation_result.score if result.validation_result else None,
                "retry_count": result.retry_count,
                "execution_time": result.metadata.get("execution_time", 0) if result.metadata else 0
            }
            
            if result.generation_result:
                step_metric.update({
                    "model": result.generation_result.model,
                    "tokens": result.generation_result.total_tokens,
                    "cost": result.generation_result.cost,
                    "confidence": result.generation_result.confidence_score
                })
            
            metrics["step_metrics"][step.value] = step_metric
        
        # Calculate duration
        if self.current_state.start_time:
            if self.current_state.end_time:
                duration = self.current_state.end_time - self.current_state.start_time
            else:
                duration = datetime.now() - self.current_state.start_time
            metrics["duration_seconds"] = duration.total_seconds()
        
        return metrics
    
    def export_results(self, output_dir: str) -> Dict[str, str]:
        """Export all pipeline results to files."""
        if not self.current_state:
            raise ValueError("No pipeline state to export")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        exported_files = {}
        
        # Export generated code
        if PipelineStep.CODE_GENERATION in self.current_state.step_results:
            code_result = self.current_state.step_results[PipelineStep.CODE_GENERATION]
            if code_result.data and "code" in code_result.data:
                code_file = output_path / code_result.data.get("file_name", "peripheral.cs")
                with open(code_file, 'w') as f:
                    f.write(code_result.data["code"])
                exported_files["code"] = str(code_file)
        
        # Export validation report
        validation_report = self.validation_engine.get_validation_report()
        report_file = output_path / f"{self.current_state.peripheral_name}_validation.json"
        with open(report_file, 'w') as f:
            json.dump(validation_report, f, indent=2)
        exported_files["validation_report"] = str(report_file)
        
        # Export pipeline state
        state_file = output_path / f"{self.current_state.peripheral_name}_pipeline_state.json"
        with open(state_file, 'w') as f:
            json.dump(self.current_state.to_dict(), f, indent=2)
        exported_files["pipeline_state"] = str(state_file)
        
        # Export metrics
        metrics_file = output_path / f"{self.current_state.peripheral_name}_metrics.json"
        with open(metrics_file, 'w') as f:
            json.dump(self.get_pipeline_metrics(), f, indent=2)
        exported_files["metrics"] = str(metrics_file)
        
        self.logger.info(f"Exported {len(exported_files)} files to {output_dir}")
        
        return exported_files
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.executor.shutdown(wait=True)
        self.model_manager.shutdown()
        if self.rag_handler:
            self.rag_handler.disconnect()


# Example usage
if __name__ == "__main__":
    import asyncio
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    async def main():
        # Initialize pipeline
        pipeline = GenerationPipeline("config.yaml")
        
        # Run pipeline
        result = await pipeline.run_pipeline(
            peripheral_name="Timer32",
            documentation_path="docs/timer32_documentation.md"
        )
        
        # Export results
        if result.status == PipelineStatus.COMPLETED:
            exported = pipeline.export_results("output")
            print(f"Results exported to: {exported}")
        
        # Print metrics
        metrics = pipeline.get_pipeline_metrics()
        print(f"\nPipeline Metrics:")
        print(f"  Status: {metrics['status']}")
        print(f"  Total Cost: ${metrics['total_cost']:.4f}")
        print(f"  Total Tokens: {metrics['total_tokens']}")
        print(f"  Duration: {metrics.get('duration_seconds', 0):.1f}s")
        
        # Cleanup
        pipeline.cleanup()
    
    # Run the async main function
    asyncio.run(main())