"""
Todo List Processing and Chain-of-Thought Generation

This module handles the generation and processing of structured todo lists
for peripheral model implementation. It uses chain-of-thought reasoning
to break down complex peripheral specifications into actionable tasks.

Key features:
- Structured todo list generation from documentation
- Chain-of-thought reasoning for task decomposition
- Task dependency analysis and ordering
- Priority assignment based on implementation complexity
- Progress tracking and task validation
- Section-by-section implementation tracking
- Todo completion verification
- Template-based generation for different peripheral types

Author: Renode Model Generator Team
Version: 2.0.0
"""

import json
import logging
import re
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskStatus(Enum):
    """Task completion status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    VERIFIED = "verified"


class TaskSection(Enum):
    """Code section categories for implementation."""
    HEADER = "header"
    IMPORTS = "imports"
    CLASS_DECLARATION = "class_declaration"
    CONSTRUCTOR = "constructor"
    REGISTERS = "registers"
    PROPERTIES = "properties"
    METHODS = "methods"
    HELPERS = "helpers"
    RESET = "reset"
    INTERRUPTS = "interrupts"
    DMA = "dma"
    VALIDATION = "validation"


@dataclass
class TodoTask:
    """Represents a single todo task."""
    id: str
    title: str
    description: str
    category: str
    section: Optional[TaskSection] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    subtasks: List['TodoTask'] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    estimated_complexity: int = 1  # 1-5 scale
    estimated_hours: float = 1.0
    reasoning: str = ""
    validation_criteria: List[str] = field(default_factory=list)
    implementation_notes: List[str] = field(default_factory=list)
    code_reference: Optional[str] = None
    completion_percentage: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "section": self.section.value if self.section else None,
            "priority": self.priority.value,
            "dependencies": self.dependencies,
            "subtasks": [t.to_dict() for t in self.subtasks],
            "status": self.status.value,
            "estimated_complexity": self.estimated_complexity,
            "estimated_hours": self.estimated_hours,
            "reasoning": self.reasoning,
            "validation_criteria": self.validation_criteria,
            "implementation_notes": self.implementation_notes,
            "code_reference": self.code_reference,
            "completion_percentage": self.completion_percentage,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TodoTask':
        """Create TodoTask from dictionary."""
        task = cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            priority=TaskPriority(data.get("priority", 3)),
            dependencies=data.get("dependencies", []),
            status=TaskStatus(data.get("status", "pending")),
            estimated_complexity=data.get("estimated_complexity", 1),
            estimated_hours=data.get("estimated_hours", 1.0),
            reasoning=data.get("reasoning", ""),
            validation_criteria=data.get("validation_criteria", []),
            implementation_notes=data.get("implementation_notes", []),
            code_reference=data.get("code_reference"),
            completion_percentage=data.get("completion_percentage", 0.0),
            metadata=data.get("metadata", {})
        )
        
        if data.get("section"):
            task.section = TaskSection(data["section"])
        
        # Recursively create subtasks
        task.subtasks = [cls.from_dict(st) for st in data.get("subtasks", [])]
        
        return task


@dataclass
class ImplementationProgress:
    """Tracks implementation progress across sections."""
    section: TaskSection
    total_tasks: int = 0
    completed_tasks: int = 0
    verified_tasks: int = 0
    completion_percentage: float = 0.0
    issues: List[str] = field(default_factory=list)
    
    def update_progress(self) -> None:
        """Update completion percentage."""
        if self.total_tasks > 0:
            self.completion_percentage = (self.completed_tasks / self.total_tasks) * 100


class TodoProcessor:
    """Processes and manages todo lists for peripheral generation."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize todo processor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load todo templates
        self.templates = self._load_templates()
        
        # Task categories
        self.categories = [
            "analysis",
            "interface_design", 
            "register_definition",
            "implementation",
            "testing",
            "documentation",
            "validation",
            "optimization"
        ]
        
        # Section mapping for code generation
        self.section_mapping = {
            "header": TaskSection.HEADER,
            "imports": TaskSection.IMPORTS,
            "class": TaskSection.CLASS_DECLARATION,
            "constructor": TaskSection.CONSTRUCTOR,
            "registers": TaskSection.REGISTERS,
            "properties": TaskSection.PROPERTIES,
            "methods": TaskSection.METHODS,
            "reset": TaskSection.RESET,
            "interrupts": TaskSection.INTERRUPTS,
            "dma": TaskSection.DMA
        }
        
        # Task ID counter
        self.task_counter = 0
        
        # Progress tracking
        self.progress_tracker: Dict[str, ImplementationProgress] = {}
        
        # Chain-of-thought patterns
        self.cot_patterns = self._load_cot_patterns()
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load todo templates from directory."""
        templates = {}
        
        # Built-in templates for different peripheral types
        templates["gpio"] = self._get_gpio_template()
        templates["timer"] = self._get_timer_template()
        templates["uart"] = self._get_uart_template()
        templates["dma"] = self._get_dma_template()
        templates["interrupt_controller"] = self._get_interrupt_controller_template()
        templates["generic"] = self._get_generic_template()
        
        # Load custom templates from directory if exists
        template_dir = Path(self.config.get("template_directory", "todo_templates"))
        
        if template_dir.exists():
            for template_file in template_dir.glob("*.json"):
                try:
                    with open(template_file, 'r') as f:
                        template_name = template_file.stem
                        templates[template_name] = json.load(f)
                        self.logger.info(f"Loaded todo template: {template_name}")
                except Exception as e:
                    self.logger.error(f"Error loading template {template_file}: {e}")
        
        return templates
    
    def _load_cot_patterns(self) -> Dict[str, List[str]]:
        """Load chain-of-thought reasoning patterns."""
        return {
            "register_implementation": [
                "Identify register purpose and functionality",
                "Map register fields to C# properties",
                "Determine access permissions and side effects",
                "Implement read/write handlers with validation",
                "Add logging for debugging",
                "Test edge cases and error conditions"
            ],
            "interrupt_handling": [
                "Identify interrupt sources and triggers",
                "Design interrupt state management",
                "Implement interrupt enable/disable logic",
                "Create interrupt status tracking",
                "Add interrupt clearing mechanisms",
                "Test interrupt generation and handling"
            ],
            "state_machine": [
                "Define all possible states",
                "Map state transitions and triggers",
                "Implement state validation logic",
                "Add state change notifications",
                "Handle invalid state transitions",
                "Test all state paths"
            ]
        }
    
    def generate_todo_list(
        self,
        peripheral_name: str,
        context_summary: str,
        documentation: str,
        peripheral_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate structured todo list for peripheral implementation.
        
        Args:
            peripheral_name: Name of the peripheral
            context_summary: Summarized context from documentation
            documentation: Raw documentation text
            peripheral_type: Optional peripheral type for template selection
            
        Returns:
            List of todo tasks
        """
        self.logger.info(f"Generating todo list for {peripheral_name}")
        
        # Reset task counter for new peripheral
        self.task_counter = 0
        
        # Extract key information from documentation
        peripheral_info = self._extract_peripheral_info(documentation)
        
        # Select appropriate template
        template = self._select_template(peripheral_type, peripheral_info)
        
        # Generate tasks based on template and extracted info
        tasks = []
        
        # Analysis tasks
        tasks.extend(self._generate_analysis_tasks(peripheral_name, peripheral_info, template))
        
        # Interface design tasks
        tasks.extend(self._generate_interface_tasks(peripheral_name, peripheral_info, template))
        
        # Register definition tasks
        tasks.extend(self._generate_register_tasks(peripheral_name, peripheral_info, template))
        
        # Implementation tasks (section-aware)
        tasks.extend(self._generate_implementation_tasks(peripheral_name, peripheral_info, template))
        
        # Testing tasks
        tasks.extend(self._generate_testing_tasks(peripheral_name, peripheral_info, template))
        
        # Documentation tasks
        tasks.extend(self._generate_documentation_tasks(peripheral_name, template))
        
        # Validation tasks
        tasks.extend(self._generate_validation_tasks(peripheral_name, template))
        
        # Optimization tasks
        tasks.extend(self._generate_optimization_tasks(peripheral_name, peripheral_info))
        
        # Analyze dependencies
        self._analyze_and_set_dependencies(tasks)
        
        # Sort by priority and dependencies
        sorted_tasks = self._topological_sort_tasks(tasks)
        
        # Initialize progress tracking
        self._initialize_progress_tracking(sorted_tasks)
        
        # Convert to dictionary format
        return [task.to_dict() for task in sorted_tasks]
    
    def generate_chain_of_thought(
        self,
        todo_list: List[Dict[str, Any]],
        peripheral_name: str
    ) -> Dict[str, Any]:
        """
        Generate chain-of-thought reasoning for todo list.
        
        Args:
            todo_list: Generated todo list
            peripheral_name: Name of the peripheral
            
        Returns:
            Chain-of-thought analysis
        """
        cot = {
            "peripheral": peripheral_name,
            "timestamp": datetime.now().isoformat(),
            "reasoning_steps": [],
            "implementation_strategy": "",
            "section_strategies": {},
            "potential_challenges": [],
            "optimization_opportunities": [],
            "estimated_total_hours": 0.0,
            "critical_path": []
        }
        
        # Analyze each task category
        for category in self.categories:
            category_tasks = [t for t in todo_list if t["category"] == category]
            if category_tasks:
                reasoning = self._generate_category_reasoning(category, category_tasks)
                cot["reasoning_steps"].append(reasoning)
        
        # Generate section-specific strategies
        for section in TaskSection:
            section_tasks = [t for t in todo_list if t.get("section") == section.value]
            if section_tasks:
                strategy = self._generate_section_strategy(section, section_tasks)
                cot["section_strategies"][section.value] = strategy
        
        # Generate overall implementation strategy
        cot["implementation_strategy"] = self._generate_implementation_strategy(todo_list)
        
        # Identify challenges
        cot["potential_challenges"] = self._identify_challenges(todo_list, peripheral_name)
        
        # Identify optimization opportunities
        cot["optimization_opportunities"] = self._identify_optimizations(todo_list)
        
        # Calculate total estimated hours
        cot["estimated_total_hours"] = sum(t.get("estimated_hours", 1.0) for t in todo_list)
        
        # Find critical path
        cot["critical_path"] = self._find_critical_path(todo_list)
        
        return cot
    
    def process_todo_section(
        self,
        todo_list: List[Dict[str, Any]],
        section: TaskSection,
        generated_code: str
    ) -> Dict[str, Any]:
        """
        Process a specific section of todos and verify implementation.
        
        Args:
            todo_list: Complete todo list
            section: Section to process
            generated_code: Generated code for the section
            
        Returns:
            Processing result with verification status
        """
        result = {
            "section": section.value,
            "tasks_processed": [],
            "completion_status": {},
            "verification_results": [],
            "missing_implementations": [],
            "code_references": {}
        }
        
        # Get tasks for this section
        section_tasks = [
            TodoTask.from_dict(t) for t in todo_list 
            if t.get("section") == section.value
        ]
        
        # Process each task
        for task in section_tasks:
            task_result = self._process_single_task(task, generated_code)
            result["tasks_processed"].append(task.id)
            result["completion_status"][task.id] = task_result["completed"]
            
            if task_result["completed"]:
                result["code_references"][task.id] = task_result.get("code_reference", "")
            else:
                result["missing_implementations"].append({
                    "task_id": task.id,
                    "title": task.title,
                    "reason": task_result.get("reason", "Not found in code")
                })
            
            # Add verification results
            if task_result.get("verification"):
                result["verification_results"].append(task_result["verification"])
        
        # Update progress tracking
        self._update_section_progress(section, result)
        
        return result
    
    def verify_todo_completion(
        self,
        todo_list: List[Dict[str, Any]],
        generated_code: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Verify that all todos have been completed in the generated code.
        
        Args:
            todo_list: Complete todo list
            generated_code: Dictionary of section name to generated code
            
        Returns:
            Verification report
        """
        report = {
            "total_tasks": len(todo_list),
            "completed_tasks": 0,
            "verified_tasks": 0,
            "pending_tasks": 0,
            "completion_percentage": 0.0,
            "section_reports": {},
            "missing_critical": [],
            "warnings": [],
            "suggestions": []
        }
        
        # Process each section
        for section in TaskSection:
            if section.value in generated_code:
                section_result = self.process_todo_section(
                    todo_list,
                    section,
                    generated_code[section.value]
                )
                report["section_reports"][section.value] = section_result
        
        # Calculate overall statistics
        for task_dict in todo_list:
            task = TodoTask.from_dict(task_dict)
            
            if task.status == TaskStatus.COMPLETED:
                report["completed_tasks"] += 1
            elif task.status == TaskStatus.VERIFIED:
                report["verified_tasks"] += 1
            else:
                report["pending_tasks"] += 1
                
                # Check if critical task is missing
                if task.priority == TaskPriority.CRITICAL:
                    report["missing_critical"].append({
                        "id": task.id,
                        "title": task.title,
                        "section": task.section.value if task.section else "unknown"
                    })
        
        # Calculate completion percentage
        if report["total_tasks"] > 0:
            report["completion_percentage"] = (
                (report["completed_tasks"] + report["verified_tasks"]) / 
                report["total_tasks"] * 100
            )
        
        # Generate warnings and suggestions
        report["warnings"] = self._generate_completion_warnings(report)
        report["suggestions"] = self._generate_completion_suggestions(report)
        
        return report
    
    def get_progress_report(self, todo_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate detailed progress report for todo list.
        
        Args:
            todo_list: Current todo list
            
        Returns:
            Progress report
        """
        total_tasks = len(todo_list)
        status_counts = defaultdict(int)
        section_progress = defaultdict(lambda: {"total": 0, "completed": 0})
        category_progress = defaultdict(lambda: {"total": 0, "completed": 0})
        
        # Calculate statistics
        total_hours_estimated = 0.0
        total_hours_completed = 0.0
        
        for task_dict in todo_list:
            task = TodoTask.from_dict(task_dict)
            status_counts[task.status.value] += 1
            
            # Section progress
            if task.section:
                section_progress[task.section.value]["total"] += 1
                if task.status in [TaskStatus.COMPLETED, TaskStatus.VERIFIED]:
                    section_progress[task.section.value]["completed"] += 1
            
            # Category progress
            category_progress[task.category]["total"] += 1
            if task.status in [TaskStatus.COMPLETED, TaskStatus.VERIFIED]:
                category_progress[task.category]["completed"] += 1
            
            # Hours tracking
            total_hours_estimated += task.estimated_hours
            if task.status in [TaskStatus.COMPLETED, TaskStatus.VERIFIED]:
                total_hours_completed += task.estimated_hours
        
        # Calculate percentages
        completed = status_counts.get("completed", 0) + status_counts.get("verified", 0)
        in_progress = status_counts.get("in_progress", 0)
        
        # Build report
        report = {
            "total_tasks": total_tasks,
            "completed": completed,
            "in_progress": in_progress,
            "pending": status_counts.get("pending", 0),
            "blocked": status_counts.get("blocked", 0),
            "completion_percentage": (completed / total_tasks * 100) if total_tasks > 0 else 0,
            "status_breakdown": dict(status_counts),
            "section_progress": dict(section_progress),
            "category_progress": dict(category_progress),
            "estimated_hours": {
                "total": total_hours_estimated,
                "completed": total_hours_completed,
                "remaining": total_hours_estimated - total_hours_completed
            },
            "critical_tasks": self._get_critical_task_status(todo_list),
            "blockers": self._identify_blockers(todo_list),
            "next_tasks": self._get_next_tasks(todo_list, limit=5)
        }
        
        return report
    
    def update_task_status(
        self,
        todo_list: List[Dict[str, Any]],
        task_id: str,
        new_status: TaskStatus,
        notes: Optional[str] = None
    ) -> bool:
        """
        Update task status with optional notes.
        
        Args:
            todo_list: Current todo list
            task_id: ID of task to update
            new_status: New status
            notes: Optional implementation notes
            
        Returns:
            True if update successful
        """
        for task_dict in todo_list:
            if task_dict["id"] == task_id:
                task_dict["status"] = new_status.value
                
                if notes:
                    if "implementation_notes" not in task_dict:
                        task_dict["implementation_notes"] = []
                    task_dict["implementation_notes"].append(notes)
                
                # Update completion percentage
                if new_status == TaskStatus.COMPLETED:
                    task_dict["completion_percentage"] = 100.0
                elif new_status == TaskStatus.IN_PROGRESS:
                    task_dict["completion_percentage"] = 50.0
                
                self.logger.info(f"Updated task {task_id} to status {new_status.value}")
                return True
        
        return False
    
    # Template methods for different peripheral types
    
    def _get_gpio_template(self) -> Dict[str, Any]:
        """Get GPIO peripheral template."""
        return {
            "name": "GPIO",
            "sections": {
                "registers": ["DATA", "DIR", "INTCFG", "INTSTAT"],
                "features": ["pin_control", "interrupts", "pull_resistors"],
                "methods": ["SetPin", "GetPin", "ConfigureInterrupt"]
            },
            "priorities": {
                "pin_control": TaskPriority.CRITICAL,
                "interrupts": TaskPriority.HIGH,
                "pull_resistors": TaskPriority.MEDIUM
            }
        }
    
    def _get_timer_template(self) -> Dict[str, Any]:
        """Get Timer peripheral template."""
        return {
            "name": "Timer",
            "sections": {
                "registers": ["CTRL", "COUNT", "COMPARE", "STATUS"],
                "features": ["counting", "compare_match", "interrupts", "prescaler"],
                "methods": ["Start", "Stop", "SetCompare", "GetCount"]
            },
            "priorities": {
                "counting": TaskPriority.CRITICAL,
                "compare_match": TaskPriority.HIGH,
                "interrupts": TaskPriority.HIGH,
                "prescaler": TaskPriority.MEDIUM
            }
        }
    
    def _get_uart_template(self) -> Dict[str, Any]:
        """Get UART peripheral template."""
        return {
            "name": "UART",
            "sections": {
                "registers": ["DATA", "CTRL", "STATUS", "BAUD"],
                "features": ["transmit", "receive", "interrupts", "flow_control", "fifo"],
                "methods": ["WriteChar", "ReadChar", "SetBaudRate", "EnableInterrupt"]
            },
            "priorities": {
                "transmit": TaskPriority.CRITICAL,
                "receive": TaskPriority.CRITICAL,
                "interrupts": TaskPriority.HIGH,
                "flow_control": TaskPriority.MEDIUM,
                "fifo": TaskPriority.MEDIUM
            }
        }
    
    def _get_dma_template(self) -> Dict[str, Any]:
        """Get DMA controller template."""
        return {
            "name": "DMA",
            "sections": {
                "registers": ["CTRL", "SRC", "DST", "COUNT", "STATUS"],
                "features": ["transfer", "channels", "interrupts", "priority", "burst"],
                "methods": ["StartTransfer", "StopTransfer", "ConfigureChannel"]
            },
            "priorities": {
                "transfer": TaskPriority.CRITICAL,
                "channels": TaskPriority.CRITICAL,
                "interrupts": TaskPriority.HIGH,
                "priority": TaskPriority.MEDIUM,
                "burst": TaskPriority.LOW
            }
        }
    
    def _get_interrupt_controller_template(self) -> Dict[str, Any]:
        """Get Interrupt Controller template."""
        return {
            "name": "InterruptController",
            "sections": {
                "registers": ["ENABLE", "PENDING", "PRIORITY", "VECTOR"],
                "features": ["enable_disable", "priority", "nesting", "vectoring"],
                "methods": ["EnableInterrupt", "SetPriority", "HandleInterrupt"]
            },
            "priorities": {
                "enable_disable": TaskPriority.CRITICAL,
                "priority": TaskPriority.HIGH,
                "nesting": TaskPriority.MEDIUM,
                "vectoring": TaskPriority.HIGH
            }
        }
    
    def _get_generic_template(self) -> Dict[str, Any]:
        """Get generic peripheral template."""
        return {
            "name": "Generic",
            "sections": {
                "registers": ["CTRL", "STATUS", "DATA"],
                "features": ["basic_control", "status_monitoring", "data_transfer"],
                "methods": ["Initialize", "Reset", "Process"]
            },
            "priorities": {
                "basic_control": TaskPriority.HIGH,
                "status_monitoring": TaskPriority.MEDIUM,
                "data_transfer": TaskPriority.HIGH
            }
        }
    
    # Helper methods
    
    def _select_template(
        self,
        peripheral_type: Optional[str],
        peripheral_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Select appropriate template based on peripheral type."""
        if peripheral_type and peripheral_type.lower() in self.templates:
            return self.templates[peripheral_type.lower()]
        
        # Try to infer from peripheral info
        interfaces = peripheral_info.get("interfaces", [])
        features = peripheral_info.get("features", [])
        
        if "gpio" in str(interfaces).lower() or "pin" in str(features).lower():
            return self.templates["gpio"]
        elif "timer" in str(interfaces).lower() or "counter" in str(features).lower():
            return self.templates["timer"]
        elif "uart" in str(interfaces).lower() or "serial" in str(features).lower():
            return self.templates["uart"]
        elif "dma" in str(interfaces).lower() or "direct memory" in str(features).lower():
            return self.templates["dma"]
        elif "interrupt" in str(interfaces).lower() and "controller" in str(features).lower():
            return self.templates["interrupt_controller"]
        
        return self.templates["generic"]
    
    def _extract_peripheral_info(self, documentation: str) -> Dict[str, Any]:
        """
        Extract key peripheral information from documentation.
        
        Args:
            documentation: Raw documentation text
            
        Returns:
            Extracted peripheral information
        """
        info = {
            "registers": [],
            "interrupts": [],
            "dma_support": False,
            "clock_domains": [],
            "interfaces": [],
            "features": [],
            "register_groups": defaultdict(list)
        }
        
        # Enhanced extraction with regex patterns
        lines = documentation.split('\n')
        
        # Register extraction with grouping
        register_pattern = re.compile(
            r'(?:register|reg)\s+(\w+).*?(?:address|offset|addr).*?(0x[0-9a-fA-F]+)',
            re.IGNORECASE
        )
        
        for i, line in enumerate(lines):
            # Extract registers
            reg_match = register_pattern.search(line)
            if reg_match:
                reg_name = reg_match.group(1)
                reg_addr = reg_match.group(2)
                info["registers"].append({
                    "name": reg_name,
                    "address": reg_addr,
                    "line": i
                })
                
                # Group registers by prefix
                prefix = reg_name.split('_')[0] if '_' in reg_name else reg_name[:3]
                info["register_groups"][prefix].append(reg_name)
            
            # Extract interrupts
            if 'interrupt' in line.lower() or 'irq' in line.lower():
                irq_match = re.search(r'(\w+).*?(?:irq|interrupt).*?(\d+)', line, re.IGNORECASE)
                if irq_match:
                    info["interrupts"].append({
                        "name": irq_match.group(1),
                        "number": int(irq_match.group(2))
                    })
            
            # Check for DMA
            if 'dma' in line.lower() or 'direct memory access' in line.lower():
                info["dma_support"] = True
            
            # Extract clock domains
            clock_match = re.search(r'(\w+)(?:_clk|_clock|clk)', line, re.IGNORECASE)
            if clock_match:
                info["clock_domains"].append(clock_match.group(1))
            
            # Extract interface types
            for interface in ['spi', 'i2c', 'uart', 'gpio', 'can', 'ethernet', 'usb', 'pcie']:
                if interface in line.lower():
                    info["interfaces"].append(interface.upper())
            
            # Extract features
            feature_keywords = [
                'fifo', 'buffer', 'prescaler', 'divider', 'counter',
                'pwm', 'capture', 'compare', 'watchdog', 'timeout'
            ]
            for feature in feature_keywords:
                if feature in line.lower():
                    info["features"].append(feature)
        
        # Deduplicate
        info["interfaces"] = list(set(info["interfaces"]))
        info["features"] = list(set(info["features"]))
        info["clock_domains"] = list(set(info["clock_domains"]))
        
        return info
    
    def _generate_analysis_tasks(
        self,
        peripheral_name: str,
        peripheral_info: Dict[str, Any],
        template: Dict[str, Any]
    ) -> List[TodoTask]:
        """Generate analysis phase tasks."""
        tasks = []
        
        # Main analysis task
        main_task = TodoTask(
            id=self._get_next_task_id(),
            title=f"Analyze {peripheral_name} specification",
            description=f"Thoroughly analyze the {peripheral_name} peripheral specification to understand all features, registers, and behaviors",
            category="analysis",
            priority=TaskPriority.CRITICAL,
            estimated_complexity=3,
            estimated_hours=2.0,
            reasoning="Understanding the peripheral specification is fundamental to correct implementation",
            validation_criteria=[
                "All registers identified and documented",
                "All operating modes understood",
                "Timing requirements captured",
                "Interface protocols documented"
            ]
        )
        
        # Add subtasks based on peripheral info
        if peripheral_info["registers"]:
            main_task.subtasks.append(TodoTask(
                id=self._get_next_task_id(),
                title="Map register addresses and bit fields",
                description="Create comprehensive mapping of all registers, their addresses, and bit field definitions",
                category="analysis",
                priority=TaskPriority.HIGH,
                estimated_complexity=2,
                estimated_hours=1.5,
                validation_criteria=[
                    "All register addresses verified",
                    "Bit field positions documented",
                    "Access permissions identified"
                ]
            ))
        
        if peripheral_info["interrupts"]:
            main_task.subtasks.append(TodoTask(
                id=self._get_next_task_id(),
                title="Analyze interrupt behavior",
                description="Document all interrupt sources, triggers, and clearing mechanisms",
                category="analysis",
                priority=TaskPriority.HIGH,
                estimated_complexity=2,
                estimated_hours=1.0
            ))
        
        if peripheral_info["dma_support"]:
            main_task.subtasks.append(TodoTask(
                id=self._get_next_task_id(),
                title="Analyze DMA capabilities",
                description="Understand DMA channels, transfer modes, and configuration",
                category="analysis",
                priority=TaskPriority.HIGH,
                estimated_complexity=3,
                estimated_hours=1.5
            ))
        
        tasks.append(main_task)
        return tasks
    
    def _generate_interface_tasks(
        self,
        peripheral_name: str,
        peripheral_info: Dict[str, Any],
        template: Dict[str, Any]
    ) -> List[TodoTask]:
        """Generate interface design tasks."""
        tasks = []
        
        task = TodoTask(
            id=self._get_next_task_id(),
            title=f"Design {peripheral_name} public interface",
            description="Design the public API that will be exposed to Renode users",
            category="interface_design",
            section=TaskSection.CLASS_DECLARATION,
            priority=TaskPriority.HIGH,
            estimated_complexity=3,
            estimated_hours=2.0,
            reasoning="A well-designed interface ensures ease of use and maintainability",
            validation_criteria=[
                "All necessary operations exposed",
                "Interface follows Renode conventions",
                "Clear method naming and parameters"
            ]
        )
        
        # Add interface-specific subtasks
        for interface in peripheral_info.get("interfaces", []):
            task.subtasks.append(TodoTask(
                id=self._get_next_task_id(),
                title=f"Design {interface} interface methods",
                description=f"Define methods for {interface} operations",
                category="interface_design",
                section=TaskSection.METHODS,
                priority=TaskPriority.HIGH,
                estimated_complexity=2,
                estimated_hours=1.0
            ))
        
        tasks.append(task)
        return tasks
    
    def _generate_register_tasks(
        self,
        peripheral_name: str,
        peripheral_info: Dict[str, Any],
        template: Dict[str, Any]
    ) -> List[TodoTask]:
        """Generate register definition tasks."""
        tasks = []
        
        main_task = TodoTask(
            id=self._get_next_task_id(),
            title="Define register structure",
            description="Create comprehensive register definitions with proper access controls",
            category="register_definition",
            section=TaskSection.REGISTERS,
            priority=TaskPriority.CRITICAL,
            estimated_complexity=4,
            estimated_hours=3.0,
            reasoning="Registers are the primary interface between software and hardware",
            validation_criteria=[
                "All registers defined with correct addresses",
                "Access permissions properly set",
                "Reset values documented",
                "Bit fields correctly mapped"
            ]
        )
        
        # Add subtasks for register groups
        for group_name, registers in peripheral_info.get("register_groups", {}).items():
            if registers:
                main_task.subtasks.append(TodoTask(
                    id=self._get_next_task_id(),
                    title=f"Implement {group_name} register group",
                    description=f"Define registers: {', '.join(registers[:3])}{'...' if len(registers) > 3 else ''}",
                    category="register_definition",
                    section=TaskSection.REGISTERS,
                    priority=TaskPriority.HIGH,
                    estimated_complexity=2,
                    estimated_hours=1.0
                ))
        
        tasks.append(main_task)
        return tasks
    
    def _generate_implementation_tasks(
        self,
        peripheral_name: str,
        peripheral_info: Dict[str, Any],
        template: Dict[str, Any]
    ) -> List[TodoTask]:
        """Generate implementation tasks with section awareness."""
        tasks = []
        
        # Constructor implementation
        tasks.append(TodoTask(
            id=self._get_next_task_id(),
            title="Implement constructor and initialization",
            description="Create constructor with proper initialization of registers and state",
            category="implementation",
            section=TaskSection.CONSTRUCTOR,
            priority=TaskPriority.CRITICAL,
            estimated_complexity=3,
            estimated_hours=2.0,
            reasoning="Proper initialization is crucial for peripheral functionality",
            validation_criteria=[
                "RegistersCollection initialized",
                "Default state set correctly",
                "Logging configured"
            ]
        ))
        
        # Core functionality implementation
        main_task = TodoTask(
            id=self._get_next_task_id(),
            title=f"Implement {peripheral_name} core functionality",
            description="Implement the main peripheral logic following Renode patterns",
            category="implementation",
            section=TaskSection.METHODS,
            priority=TaskPriority.CRITICAL,
            estimated_complexity=5,
            estimated_hours=4.0,
            reasoning="Core implementation is the heart of the peripheral model",
            validation_criteria=[
                "All registers functional",
                "State machine implemented correctly",
                "Renode patterns followed"
            ]
        )
        
        # Add feature-specific subtasks
        for feature in template.get("sections", {}).get("features", []):
            if feature in peripheral_info.get("features", []) or feature in str(peripheral_info).lower():
                priority = template.get("priorities", {}).get(feature, TaskPriority.MEDIUM)
                main_task.subtasks.append(TodoTask(
                    id=self._get_next_task_id(),
                    title=f"Implement {feature.replace('_', ' ')} functionality",
                    description=f"Add support for {feature} feature",
                    category="implementation",
                    section=TaskSection.METHODS,
                    priority=priority,
                    estimated_complexity=3,
                    estimated_hours=2.0
                ))
        
        tasks.append(main_task)
        
        # Reset handling
        tasks.append(TodoTask(
            id=self._get_next_task_id(),
            title="Implement reset behavior",
            description="Ensure proper reset handling for all registers and state",
            category="implementation",
            section=TaskSection.RESET,
            priority=TaskPriority.HIGH,
            estimated_complexity=2,
            estimated_hours=1.0,
            reasoning="Proper reset behavior is critical for peripheral reliability"
        ))
        
        # Interrupt handling if applicable
        if peripheral_info.get("interrupts"):
            tasks.append(TodoTask(
                id=self._get_next_task_id(),
                title="Implement interrupt handling",
                description="Add interrupt generation and management logic",
                category="implementation",
                section=TaskSection.INTERRUPTS,
                priority=TaskPriority.HIGH,
                estimated_complexity=3,
                estimated_hours=2.0,
                validation_criteria=[
                    "Interrupt sources properly triggered",
                    "Interrupt clearing works correctly",
                    "Edge/level triggering implemented"
                ]
            ))
        
        # DMA handling if applicable
        if peripheral_info.get("dma_support"):
            tasks.append(TodoTask(
                id=self._get_next_task_id(),
                title="Implement DMA functionality",
                description="Add DMA transfer support with proper channel management",
                category="implementation",
                section=TaskSection.DMA,
                priority=TaskPriority.HIGH,
                estimated_complexity=4,
                estimated_hours=3.0
            ))
        
        return tasks
    
    def _generate_testing_tasks(
        self,
        peripheral_name: str,
        peripheral_info: Dict[str, Any],
        template: Dict[str, Any]
    ) -> List[TodoTask]:
        """Generate testing tasks."""
        tasks = []
        
        # Main testing task
        main_task = TodoTask(
            id=self._get_next_task_id(),
            title=f"Create comprehensive tests for {peripheral_name}",
            description="Develop unit tests covering all peripheral functionality",
            category="testing",
            priority=TaskPriority.HIGH,
            estimated_complexity=4,
            estimated_hours=3.0,
            reasoning="Thorough testing ensures peripheral reliability and correctness",
            validation_criteria=[
                "All public methods tested",
                "Edge cases covered",
                "Integration tests included"
            ]
        )
        
        # Add specific test subtasks
        main_task.subtasks.extend([
            TodoTask(
                id=self._get_next_task_id(),
                title="Test register read/write operations",
                description="Verify all registers can be read and written correctly",
                category="testing",
                priority=TaskPriority.HIGH,
                estimated_complexity=2,
                estimated_hours=1.0
            ),
            TodoTask(
                id=self._get_next_task_id(),
                title="Test reset behavior",
                description="Verify peripheral resets to correct initial state",
                category="testing",
                priority=TaskPriority.HIGH,
                estimated_complexity=2,
                estimated_hours=0.5
            )
        ])
        
        if peripheral_info.get("interrupts"):
            main_task.subtasks.append(TodoTask(
                id=self._get_next_task_id(),
                title="Test interrupt generation",
                description="Verify interrupts are generated and cleared correctly",
                category="testing",
                priority=TaskPriority.HIGH,
                estimated_complexity=3,
                estimated_hours=1.5
            ))
        
        tasks.append(main_task)
        return tasks
    
    def _generate_documentation_tasks(
        self,
        peripheral_name: str,
        template: Dict[str, Any]
    ) -> List[TodoTask]:
        """Generate documentation tasks."""
        return [
            TodoTask(
                id=self._get_next_task_id(),
                title=f"Document {peripheral_name} implementation",
                description="Create comprehensive documentation including usage examples",
                category="documentation",
                priority=TaskPriority.MEDIUM,
                estimated_complexity=3,
                estimated_hours=2.0,
                reasoning="Good documentation ensures the peripheral can be used effectively",
                validation_criteria=[
                    "API documentation complete",
                    "Usage examples provided",
                    "Integration guide included"
                ]
            )
        ]
    
    def _generate_validation_tasks(
        self,
        peripheral_name: str,
        template: Dict[str, Any]
    ) -> List[TodoTask]:
        """Generate validation tasks."""
        return [
            TodoTask(
                id=self._get_next_task_id(),
                title="Validate implementation against specification",
                description="Ensure the implementation matches the peripheral specification exactly",
                category="validation",
                section=TaskSection.VALIDATION,
                priority=TaskPriority.CRITICAL,
                estimated_complexity=3,
                estimated_hours=2.0,
                reasoning="Validation ensures correctness and specification compliance",
                validation_criteria=[
                    "All specification requirements met",
                    "No undocumented behavior",
                    "Performance requirements satisfied"
                ]
            )
        ]
    
    def _generate_optimization_tasks(
        self,
        peripheral_name: str,
        peripheral_info: Dict[str, Any]
    ) -> List[TodoTask]:
        """Generate optimization tasks."""
        tasks = []
        
        # Only add optimization tasks for complex peripherals
        if len(peripheral_info.get("registers", [])) > 10 or peripheral_info.get("dma_support"):
            tasks.append(TodoTask(
                id=self._get_next_task_id(),
                title="Optimize performance-critical paths",
                description="Profile and optimize frequently accessed code paths",
                category="optimization",
                priority=TaskPriority.LOW,
                estimated_complexity=3,
                estimated_hours=2.0,
                reasoning="Performance optimization improves simulation speed"
            ))
        
        return tasks
    
    def _analyze_and_set_dependencies(self, tasks: List[TodoTask]) -> None:
        """Analyze and set task dependencies."""
        # Create task lookup
        task_map = {task.id: task for task in tasks}
        
        # Flatten all tasks including subtasks
        all_tasks = []
        for task in tasks:
            all_tasks.append(task)
            all_tasks.extend(self._flatten_subtasks(task))
        
        # Set dependencies based on categories and sections
        category_order = {
            "analysis": 0,
            "interface_design": 1,
            "register_definition": 2,
            "implementation": 3,
            "testing": 4,
            "documentation": 5,
            "validation": 6,
            "optimization": 7
        }
        
        for task in all_tasks:
            task_order = category_order.get(task.category, 999)
            
            # Find tasks that must complete before this one
            for other_task in all_tasks:
                if other_task.id == task.id:
                    continue
                
                other_order = category_order.get(other_task.category, 999)
                
                # Add dependency if other task is in an earlier category
                if other_order < task_order:
                    # Only add direct dependencies (not transitive)
                    if other_order == task_order - 1:
                        task.dependencies.append(other_task.id)
                
                # Section-based dependencies within same category
                if task.category == other_task.category and task.section and other_task.section:
                    if self._should_depend_on_section(task.section, other_task.section):
                        task.dependencies.append(other_task.id)
    
    def _should_depend_on_section(self, section1: TaskSection, section2: TaskSection) -> bool:
        """Determine if section1 should depend on section2."""
        section_order = {
            TaskSection.HEADER: 0,
            TaskSection.IMPORTS: 1,
            TaskSection.CLASS_DECLARATION: 2,
            TaskSection.CONSTRUCTOR: 3,
            TaskSection.REGISTERS: 4,
            TaskSection.PROPERTIES: 5,
            TaskSection.METHODS: 6,
            TaskSection.HELPERS: 7,
            TaskSection.RESET: 8,
            TaskSection.INTERRUPTS: 9,
            TaskSection.DMA: 10,
            TaskSection.VALIDATION: 11
        }
        
        return section_order.get(section1, 999) > section_order.get(section2, 0)
    
    def _flatten_subtasks(self, task: TodoTask) -> List[TodoTask]:
        """Recursively flatten subtasks."""
        result = []
        for subtask in task.subtasks:
            result.append(subtask)
            result.extend(self._flatten_subtasks(subtask))
        return result
    
    def _topological_sort_tasks(self, tasks: List[TodoTask]) -> List[TodoTask]:
        """Sort tasks topologically based on dependencies."""
        # Flatten all tasks
        all_tasks = []
        for task in tasks:
            all_tasks.append(task)
            all_tasks.extend(self._flatten_subtasks(task))
        
        # Build adjacency list
        graph = {task.id: task.dependencies for task in all_tasks}
        task_map = {task.id: task for task in all_tasks}
        
        # Calculate in-degree
        in_degree = {task_id: 0 for task_id in graph}
        for task_id, deps in graph.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[dep] += 1
        
        # Find tasks with no dependencies
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        sorted_tasks = []
        
        while queue:
            # Sort queue by priority for tasks at the same level
            queue.sort(key=lambda tid: (task_map[tid].priority.value, tid))
            
            task_id = queue.pop(0)
            sorted_tasks.append(task_map[task_id])
            
            # Update in-degrees
            for other_id, deps in graph.items():
                if task_id in deps:
                    in_degree[other_id] -= 1
                    if in_degree[other_id] == 0:
                        queue.append(other_id)
        
        # Return only top-level tasks (subtasks are included within them)
        return [task for task in tasks if task in sorted_tasks]
    
    def _initialize_progress_tracking(self, tasks: List[TodoTask]) -> None:
        """Initialize progress tracking for all sections."""
        self.progress_tracker.clear()
        
        for section in TaskSection:
            progress = ImplementationProgress(section=section)
            
            # Count tasks in this section
            for task in tasks:
                if task.section == section:
                    progress.total_tasks += 1
                for subtask in self._flatten_subtasks(task):
                    if subtask.section == section:
                        progress.total_tasks += 1
            
            if progress.total_tasks > 0:
                self.progress_tracker[section.value] = progress
    
    def _process_single_task(self, task: TodoTask, generated_code: str) -> Dict[str, Any]:
        """Process a single task and check if it's implemented in the code."""
        result = {
            "completed": False,
            "code_reference": None,
            "verification": None,
            "reason": None
        }
        
        # Check for task-specific patterns in the code
        patterns = self._get_task_verification_patterns(task)
        
        for pattern in patterns:
            match = re.search(pattern, generated_code, re.MULTILINE | re.DOTALL)
            if match:
                result["completed"] = True
                result["code_reference"] = f"Line {generated_code[:match.start()].count(chr(10)) + 1}"
                result["verification"] = {
                    "task_id": task.id,
                    "pattern_matched": pattern,
                    "confidence": 0.9
                }
                break
        
        if not result["completed"]:
            result["reason"] = "No matching implementation pattern found"
        
        return result
    
    def _get_task_verification_patterns(self, task: TodoTask) -> List[str]:
        """Get regex patterns to verify task implementation."""
        patterns = []
        
        # Section-specific patterns
        if task.section == TaskSection.CONSTRUCTOR:
            patterns.append(r'public\s+\w+\s*\([^)]*Machine\s+machine[^)]*\)')
            patterns.append(r'RegistersCollection|DoubleWordRegisterCollection')
        elif task.section == TaskSection.REGISTERS:
            patterns.append(r'new\s+DoubleWordRegister\s*\(')
            patterns.append(r'\.With(?:Flag|ValueField|ReservedBits)\s*\(')
        elif task.section == TaskSection.METHODS:
            patterns.append(r'(?:public|private|protected)\s+\w+\s+\w+\s*\([^)]*\)\s*{')
        elif task.section == TaskSection.RESET:
            patterns.append(r'public\s+override\s+void\s+Reset\s*\(\s*\)')
        elif task.section == TaskSection.INTERRUPTS:
            patterns.append(r'(?:interrupt|irq|IRQ)')
            patterns.append(r'UpdateInterrupts|RaiseInterrupt')
        
        # Category-specific patterns
        if "register" in task.title.lower():
            patterns.append(r'Register|register')
        if "interface" in task.title.lower():
            patterns.append(r':\s*I\w+')
        if "test" in task.category:
            patterns.append(r'\[Test\]|\[TestCase\]')
        
        return patterns
    
    def _update_section_progress(self, section: TaskSection, result: Dict[str, Any]) -> None:
        """Update progress tracking for a section."""
        if section.value in self.progress_tracker:
            progress = self.progress_tracker[section.value]
            
            # Update completed count
            completed = sum(1 for status in result["completion_status"].values() if status)
            progress.completed_tasks = completed
            
            # Update issues
            progress.issues = [
                f"{item['title']}: {item['reason']}"
                for item in result["missing_implementations"]
            ]
            
            progress.update_progress()
    
    def _generate_category_reasoning(
        self,
        category: str,
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate reasoning for a task category."""
        reasoning = {
            "category": category,
            "task_count": len(tasks),
            "total_complexity": sum(t.get("estimated_complexity", 1) for t in tasks),
            "total_hours": sum(t.get("estimated_hours", 1.0) for t in tasks),
            "approach": "",
            "key_considerations": []
        }
        
        # Category-specific reasoning
        if category == "analysis":
            reasoning["approach"] = "Systematic analysis of documentation to extract all requirements"
            reasoning["key_considerations"] = [
                "Identify all hardware features",
                "Document timing constraints",
                "Note any ambiguities for clarification"
            ]
        elif category == "implementation":
            reasoning["approach"] = "Incremental implementation following Renode patterns"
            reasoning["key_considerations"] = [
                "Follow established Renode conventions",
                "Implement core functionality first",
                "Add advanced features incrementally"
            ]
        elif category == "testing":
            reasoning["approach"] = "Comprehensive testing with focus on edge cases"
            reasoning["key_considerations"] = [
                "Test all public interfaces",
                "Verify register behavior",
                "Test interrupt and DMA functionality"
            ]
        
        return reasoning
    
    def _generate_section_strategy(
        self,
        section: TaskSection,
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate implementation strategy for a code section."""
        strategy = {
            "section": section.value,
            "task_count": len(tasks),
            "approach": "",
            "dependencies": [],
            "patterns": []
        }
        
        # Section-specific strategies
        if section == TaskSection.CONSTRUCTOR:
            strategy["approach"] = "Initialize all components in proper order"
            strategy["patterns"] = ["RegistersCollection", "Machine parameter"]
        elif section == TaskSection.REGISTERS:
            strategy["approach"] = "Define all registers with proper bit fields"
            strategy["patterns"] = ["DoubleWordRegister", "WithFlag", "WithValueField"]
        elif section == TaskSection.METHODS:
            strategy["approach"] = "Implement core functionality with proper state management"
            strategy["patterns"] = ["State validation", "Logging", "Event handling"]
        
        return strategy
    
    def _generate_implementation_strategy(self, todo_list: List[Dict[str, Any]]) -> str:
        """Generate overall implementation strategy."""
        total_tasks = len(todo_list)
        total_complexity = sum(t.get("estimated_complexity", 1) for t in todo_list)
        total_hours = sum(t.get("estimated_hours", 1.0) for t in todo_list)
        
        # Count by category
        category_counts = defaultdict(int)
        for task in todo_list:
            category_counts[task["category"]] += 1
        
        strategy = f"""
Implementation Strategy:
1. Begin with thorough analysis phase ({category_counts['analysis']} tasks)
2. Design clean interfaces following Renode conventions ({category_counts['interface_design']} tasks)
3. Implement register definitions with proper access control ({category_counts['register_definition']} tasks)
4. Build core functionality incrementally ({category_counts['implementation']} tasks)
5. Develop comprehensive test suite in parallel ({category_counts['testing']} tasks)
6. Validate against specification continuously ({category_counts['validation']} tasks)
7. Document as implementation progresses ({category_counts['documentation']} tasks)

Total tasks: {total_tasks}
Estimated complexity: {total_complexity} units
Estimated hours: {total_hours:.1f}
Recommended approach: Iterative development with continuous validation
"""
        return strategy.strip()
    
    def _identify_challenges(
        self,
        todo_list: List[Dict[str, Any]],
        peripheral_name: str
    ) -> List[str]:
        """Identify potential implementation challenges."""
        challenges = []
        
        # High complexity tasks
        complex_tasks = [t for t in todo_list if t.get("estimated_complexity", 1) >= 4]
        if complex_tasks:
            challenges.append(f"High complexity tasks identified: {len(complex_tasks)} tasks with complexity >= 4")
        
        # Many dependencies
        high_dep_tasks = [t for t in todo_list if len(t.get("dependencies", [])) > 2]
        if high_dep_tasks:
            challenges.append(f"Complex dependency chains: {len(high_dep_tasks)} tasks with multiple dependencies")
        
        # Feature-specific challenges
        features = set()
        for task in todo_list:
            if "dma" in task.get("title", "").lower():
                features.add("dma")
            if "interrupt" in task.get("title", "").lower():
                features.add("interrupt")
            if "state machine" in task.get("description", "").lower():
                features.add("state_machine")
        
        if "dma" in features:
            challenges.append("DMA implementation requires careful memory management")
        if "interrupt" in features:
            challenges.append("Interrupt handling requires precise timing simulation")
        if "state_machine" in features:
            challenges.append("Complex state machine requires thorough testing")
        
        return challenges
    
    def _identify_optimizations(self, todo_list: List[Dict[str, Any]]) -> List[str]:
        """Identify optimization opportunities."""
        optimizations = []
        
        # Parallel task opportunities
        categories = defaultdict(int)
        for task in todo_list:
            categories[task.get("category", "unknown")] += 1
        
        if categories.get("testing", 0) > 3:
            optimizations.append("Multiple test tasks can be developed in parallel")
        
        # Reusable components
        register_count = sum(1 for t in todo_list if "register" in t.get("title", "").lower())
        if register_count > 5:
            optimizations.append("Consider creating register helper methods for common patterns")
        
        # Template usage
        if any("template" in t.get("title", "").lower() for t in todo_list):
            optimizations.append("Leverage existing Renode templates for faster implementation")
        
        # Documentation automation
        if categories.get("documentation", 0) > 0:
            optimizations.append("Generate documentation from code annotations")
        
        return optimizations
    
    def _find_critical_path(self, todo_list: List[Dict[str, Any]]) -> List[str]:
        """Find the critical path through tasks."""
        # Convert to TodoTask objects for easier processing
        tasks = [TodoTask.from_dict(t) for t in todo_list]
        task_map = {t.id: t for t in tasks}
        
        # Find longest path considering both dependencies and estimated hours
        def get_path_length(task_id: str, visited: Set[str]) -> Tuple[float, List[str]]:
            if task_id in visited or task_id not in task_map:
                return 0.0, []
            
            visited.add(task_id)
            task = task_map[task_id]
            
            max_dep_length = 0.0
            max_dep_path = []
            
            for dep in task.dependencies:
                dep_length, dep_path = get_path_length(dep, visited.copy())
                if dep_length > max_dep_length:
                    max_dep_length = dep_length
                    max_dep_path = dep_path
            
            total_length = task.estimated_hours + max_dep_length
            path = [task_id] + max_dep_path
            
            return total_length, path
        
        # Find task with longest path
        max_length = 0.0
        critical_path = []
        
        for task in tasks:
            length, path = get_path_length(task.id, set())
            if length > max_length:
                max_length = length
                critical_path = path
        
        return critical_path
    
    def _get_critical_task_status(self, todo_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get status of critical tasks."""
        critical_tasks = [
            TodoTask.from_dict(t) for t in todo_list 
            if t.get("priority") == TaskPriority.CRITICAL.value
        ]
        
        completed = sum(1 for t in critical_tasks if t.status in [TaskStatus.COMPLETED, TaskStatus.VERIFIED])
        
        return {
            "total": len(critical_tasks),
            "completed": completed,
            "pending": len(critical_tasks) - completed,
            "completion_percentage": (completed / len(critical_tasks) * 100) if critical_tasks else 100
        }
    
    def _identify_blockers(self, todo_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify tasks that are blocking others."""
        blockers = []
        task_map = {t["id"]: t for t in todo_list}
        
        # Count how many tasks depend on each task
        dependency_count = defaultdict(int)
        for task in todo_list:
            for dep in task.get("dependencies", []):
                dependency_count[dep] += 1
        
        # Find incomplete tasks that are blocking others
        for task_id, count in dependency_count.items():
            if count > 0 and task_id in task_map:
                task = task_map[task_id]
                if task["status"] not in ["completed", "verified"]:
                    blockers.append({
                        "task_id": task_id,
                        "title": task["title"],
                        "blocking_count": count,
                        "status": task["status"]
                    })
        
        # Sort by blocking count
        blockers.sort(key=lambda x: x["blocking_count"], reverse=True)
        
        return blockers
    
    def _get_next_tasks(self, todo_list: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """Get next tasks that can be started."""
        next_tasks = []
        
        for task_dict in todo_list:
            if task_dict["status"] == "pending":
                # Check if all dependencies are completed
                deps_completed = all(
                    self._is_task_completed(todo_list, dep)
                    for dep in task_dict.get("dependencies", [])
                )
                
                if deps_completed:
                    next_tasks.append({
                        "id": task_dict["id"],
                        "title": task_dict["title"],
                        "category": task_dict["category"],
                        "priority": task_dict["priority"],
                        "estimated_hours": task_dict.get("estimated_hours", 1.0)
                    })
        
        # Sort by priority
        next_tasks.sort(key=lambda x: x["priority"])
        
        return next_tasks[:limit]
    
    def _is_task_completed(self, todo_list: List[Dict[str, Any]], task_id: str) -> bool:
        """Check if a task is completed."""
        for task in todo_list:
            if task["id"] == task_id:
                return task["status"] in ["completed", "verified"]
        return False
    
    def _generate_completion_warnings(self, report: Dict[str, Any]) -> List[str]:
        """Generate warnings based on completion report."""
        warnings = []
        
        if report["missing_critical"]:
            warnings.append(f"Critical tasks missing: {len(report['missing_critical'])} tasks must be completed")
        
        if report["completion_percentage"] < 80:
            warnings.append(f"Low completion rate: {report['completion_percentage']:.1f}% - review pending tasks")
        
        # Check section completion
        for section, section_report in report.get("section_reports", {}).items():
            missing = section_report.get("missing_implementations", [])
            if missing:
                warnings.append(f"Section '{section}' has {len(missing)} incomplete tasks")
        
        return warnings
    
    def _generate_completion_suggestions(self, report: Dict[str, Any]) -> List[str]:
        """Generate suggestions for improving completion."""
        suggestions = []
        
        if report["completion_percentage"] < 100:
            remaining_hours = 0
            for section_report in report.get("section_reports", {}).values():
                # Estimate based on missing tasks
                remaining_hours += len(section_report.get("missing_implementations", [])) * 1.5
            
            suggestions.append(f"Estimated {remaining_hours:.1f} hours needed to complete remaining tasks")
        
        # Suggest focusing on critical tasks
        if report["missing_critical"]:
            suggestions.append("Focus on completing critical tasks first")
        
        # Suggest parallel work
        if report["pending_tasks"] > 5:
            suggestions.append("Consider parallel development of independent tasks")
        
        return suggestions
    
    def _get_next_task_id(self) -> str:
        """Generate next task ID."""
        self.task_counter += 1
        return f"task_{self.task_counter:04d}"