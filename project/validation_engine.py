"""
Comprehensive Validation Engine for Multi-Step Pipeline

This module provides extensive validation capabilities for the generation pipeline,
including cross-step validation, schema validation, register conflict detection,
and detailed error reporting.

Key Features:
- Step-specific validators for all 6 pipeline steps
- Register validation with bit-field overlap detection
- Cross-step consistency checking
- Detailed validation reporting with severity levels
- Schema management and custom validation rules

Author: Renode Model Generator Team
Version: 2.0.0
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set, Union
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict

import jsonschema
from jsonschema import validate, ValidationError, Draft7Validator


class Severity(Enum):
    """Validation issue severity levels."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""
    severity: Severity
    message: str
    location: Optional[str] = None
    suggestion: Optional[str] = None
    step: Optional[str] = None
    field: Optional[str] = None
    line_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "severity": self.severity.value,
            "message": self.message,
            "location": self.location,
            "suggestion": self.suggestion,
            "step": self.step,
            "field": self.field,
            "line_number": self.line_number
        }


@dataclass
class ValidationResult:
    """Comprehensive validation result."""
    valid: bool = True
    issues: List[ValidationIssue] = field(default_factory=list)
    score: float = 100.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_issue(self, issue: ValidationIssue):
        """Add a validation issue and update validity."""
        self.issues.append(issue)
        if issue.severity == Severity.ERROR:
            self.valid = False
    
    def calculate_score(self):
        """Calculate validation score based on issues."""
        if not self.issues:
            self.score = 100.0
            return
        
        error_count = sum(1 for i in self.issues if i.severity == Severity.ERROR)
        warning_count = sum(1 for i in self.issues if i.severity == Severity.WARNING)
        
        # Errors have more weight than warnings
        self.score = max(0, 100 - (error_count * 10) - (warning_count * 2))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "valid": self.valid,
            "issues": [issue.to_dict() for issue in self.issues],
            "score": self.score,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "error_count": sum(1 for i in self.issues if i.severity == Severity.ERROR),
            "warning_count": sum(1 for i in self.issues if i.severity == Severity.WARNING),
            "info_count": sum(1 for i in self.issues if i.severity == Severity.INFO)
        }


@dataclass
class RegisterInfo:
    """Register information for validation."""
    name: str
    address: int
    size: int = 4  # Default 32-bit
    access: str = "RW"
    reset_value: Optional[int] = None
    bit_fields: List[Dict[str, Any]] = field(default_factory=list)
    description: Optional[str] = None


class BaseValidator:
    """Base class for step-specific validators."""
    
    def __init__(self, schema_path: Optional[Path] = None):
        """Initialize validator with optional schema."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.schema = None
        if schema_path and schema_path.exists():
            with open(schema_path, 'r') as f:
                self.schema = json.load(f)
                self.json_validator = Draft7Validator(self.schema)
    
    def validate(self, data: Any) -> ValidationResult:
        """Validate data and return result."""
        result = ValidationResult()
        
        # Schema validation if available
        if self.schema:
            self._validate_schema(data, result)
        
        # Custom validation logic
        self._validate_custom(data, result)
        
        # Calculate final score
        result.calculate_score()
        
        return result
    
    def _validate_schema(self, data: Any, result: ValidationResult):
        """Validate against JSON schema."""
        try:
            errors = list(self.json_validator.iter_errors(data))
            for error in errors:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Schema validation failed: {error.message}",
                    location=".".join(str(p) for p in error.path),
                    field=error.path[-1] if error.path else None
                ))
        except Exception as e:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Schema validation error: {str(e)}"
            ))
    
    def _validate_custom(self, data: Any, result: ValidationResult):
        """Override in subclasses for custom validation logic."""
        pass


class SectionSummaryValidator(BaseValidator):
    """Validates Step 1 output - section summaries."""
    
    def _validate_custom(self, data: Any, result: ValidationResult):
        """Validate section summaries."""
        if not isinstance(data, dict):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Section summary must be a dictionary"
            ))
            return
        
        # Check required sections
        required_sections = ["overview", "registers", "functionality"]
        for section in required_sections:
            if section not in data:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Missing required section: {section}",
                    suggestion=f"Add a '{section}' section to the summary"
                ))
        
        # Validate section content
        for section_name, content in data.items():
            if not content or (isinstance(content, str) and len(content.strip()) < 10):
                result.add_issue(ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Section '{section_name}' has insufficient content",
                    location=section_name,
                    suggestion="Provide more detailed information in this section"
                ))


class DataExtractionValidator(BaseValidator):
    """Validates Step 2 output - peripheral metadata."""
    
    def _validate_custom(self, data: Any, result: ValidationResult):
        """Validate extracted peripheral metadata."""
        if not isinstance(data, dict):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Peripheral metadata must be a dictionary"
            ))
            return
        
        # Validate peripheral name
        if "peripheral_name" not in data:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Missing peripheral name",
                suggestion="Add 'peripheral_name' field"
            ))
        elif not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', data.get("peripheral_name", "")):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Invalid peripheral name: {data.get('peripheral_name')}",
                suggestion="Use valid identifier format (letters, numbers, underscore)"
            ))
        
        # Validate base address
        if "base_address" in data:
            try:
                addr = int(str(data["base_address"]), 0)
                if addr % 4 != 0:
                    result.add_issue(ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"Base address 0x{addr:X} is not 4-byte aligned",
                        suggestion="Align base address to 4-byte boundary"
                    ))
            except (ValueError, TypeError):
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Invalid base address format: {data['base_address']}"
                ))
        
        # Validate interrupts
        if "interrupts" in data:
            for idx, interrupt in enumerate(data["interrupts"]):
                if not isinstance(interrupt, dict):
                    result.add_issue(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Interrupt {idx} must be a dictionary",
                        location=f"interrupts[{idx}]"
                    ))
                elif "name" not in interrupt or "number" not in interrupt:
                    result.add_issue(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Interrupt {idx} missing required fields",
                        location=f"interrupts[{idx}]",
                        suggestion="Add 'name' and 'number' fields"
                    ))


class RegisterMappingValidator(BaseValidator):
    """Validates Step 3 output - register details (MOST CRITICAL)."""
    
    def _validate_custom(self, data: Any, result: ValidationResult):
        """Validate register mappings with extensive checks."""
        if not isinstance(data, dict) or "registers" not in data:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Register mapping must contain 'registers' field"
            ))
            return
        
        registers = data["registers"]
        if not isinstance(registers, list):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Registers must be a list"
            ))
            return
        
        # Track addresses for conflict detection
        address_map: Dict[int, RegisterInfo] = {}
        
        for idx, register in enumerate(registers):
            reg_info = self._validate_single_register(register, idx, result)
            if reg_info:
                # Check for address conflicts
                self._check_address_conflicts(reg_info, address_map, result)
                
                # Validate bit fields
                if reg_info.bit_fields:
                    self._validate_bit_fields(reg_info, result)
    
    def _validate_single_register(self, register: Dict[str, Any], idx: int, 
                                 result: ValidationResult) -> Optional[RegisterInfo]:
        """Validate a single register definition."""
        location = f"registers[{idx}]"
        
        # Check required fields
        required_fields = ["name", "address", "size", "access"]
        for field in required_fields:
            if field not in register:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Register missing required field: {field}",
                    location=location,
                    field=field
                ))
                return None
        
        # Validate register name
        name = register["name"]
        if not re.match(r'^[A-Z][A-Z0-9_]*$', name):
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                message=f"Register name '{name}' doesn't follow naming convention",
                location=location,
                suggestion="Use UPPER_SNAKE_CASE for register names"
            ))
        
        # Validate address
        try:
            address = int(str(register["address"]), 0)
        except (ValueError, TypeError):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Invalid address format for register {name}",
                location=location
            ))
            return None
        
        # Validate size
        size = register["size"]
        if size not in [8, 16, 32]:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Invalid register size {size} for {name}",
                location=location,
                suggestion="Use 8, 16, or 32 bit register size"
            ))
            return None
        
        # Validate access permissions
        access = register["access"].upper()
        if access not in ["RO", "WO", "RW", "W1C", "W1S", "RC"]:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Invalid access permission '{access}' for {name}",
                location=location,
                suggestion="Use RO, WO, RW, W1C, W1S, or RC"
            ))
        
        # Validate reset value
        reset_value = None
        if "reset_value" in register:
            try:
                reset_value = int(str(register["reset_value"]), 0)
                max_value = (1 << size) - 1
                if reset_value > max_value:
                    result.add_issue(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Reset value 0x{reset_value:X} exceeds {size}-bit range for {name}",
                        location=location,
                        suggestion=f"Use value between 0x0 and 0x{max_value:X}"
                    ))
            except (ValueError, TypeError):
                result.add_issue(ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Invalid reset value format for {name}",
                    location=location
                ))
        
        return RegisterInfo(
            name=name,
            address=address,
            size=size,
            access=access,
            reset_value=reset_value,
            bit_fields=register.get("bit_fields", []),
            description=register.get("description")
        )
    
    def _check_address_conflicts(self, reg_info: RegisterInfo, 
                                address_map: Dict[int, RegisterInfo], 
                                result: ValidationResult):
        """Check for register address conflicts and overlaps."""
        start_addr = reg_info.address
        end_addr = start_addr + (reg_info.size // 8) - 1
        
        for addr in range(start_addr, end_addr + 1):
            if addr in address_map:
                existing = address_map[addr]
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Register '{reg_info.name}' at 0x{start_addr:X} conflicts with "
                           f"'{existing.name}' at 0x{existing.address:X}",
                    suggestion="Adjust register addresses to avoid overlap"
                ))
                return
        
        # Add to address map
        for addr in range(start_addr, end_addr + 1):
            address_map[addr] = reg_info
    
    def _validate_bit_fields(self, reg_info: RegisterInfo, result: ValidationResult):
        """Validate bit fields within a register."""
        bit_fields = reg_info.bit_fields
        if not bit_fields:
            return
        
        # Track bit usage
        bit_usage = [False] * reg_info.size
        
        for idx, field in enumerate(bit_fields):
            location = f"{reg_info.name}.bit_fields[{idx}]"
            
            # Validate field structure
            if not isinstance(field, dict):
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Bit field must be a dictionary",
                    location=location
                ))
                continue
            
            # Check required fields
            if "name" not in field or "start_bit" not in field or "end_bit" not in field:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Bit field missing required fields",
                    location=location,
                    suggestion="Add 'name', 'start_bit', and 'end_bit'"
                ))
                continue
            
            name = field["name"]
            try:
                start_bit = int(field["start_bit"])
                end_bit = int(field["end_bit"])
            except (ValueError, TypeError):
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Invalid bit positions for field {name}",
                    location=location
                ))
                continue
            
            # Validate bit range
            if start_bit < 0 or end_bit >= reg_info.size:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Bit field {name} exceeds register size",
                    location=location,
                    suggestion=f"Use bits 0-{reg_info.size-1}"
                ))
                continue
            
            if start_bit > end_bit:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Invalid bit range for field {name}: {start_bit}-{end_bit}",
                    location=location,
                    suggestion="start_bit must be <= end_bit"
                ))
                continue
            
            # Check for bit overlap
            for bit in range(start_bit, end_bit + 1):
                if bit_usage[bit]:
                    result.add_issue(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Bit field {name} overlaps with another field at bit {bit}",
                        location=location,
                        suggestion="Adjust bit field ranges to avoid overlap"
                    ))
                    break
                bit_usage[bit] = True
            
            # Validate reserved bit handling
            if name.upper() in ["RESERVED", "RES", "RSVD"]:
                if field.get("access", "RO") != "RO":
                    result.add_issue(ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"Reserved field {name} should be read-only",
                        location=location,
                        suggestion="Set access to 'RO' for reserved fields"
                    ))


class ArchitectureValidator(BaseValidator):
    """Validates Step 4 output - architectural plan."""
    
    def _validate_custom(self, data: Any, result: ValidationResult):
        """Validate architectural plan."""
        if not isinstance(data, dict):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Architecture plan must be a dictionary"
            ))
            return
        
        # Check required components
        required_components = ["class_structure", "interfaces", "dependencies"]
        for component in required_components:
            if component not in data:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Missing architectural component: {component}",
                    suggestion=f"Add '{component}' to the architecture plan"
                ))
        
        # Validate class structure
        if "class_structure" in data:
            class_info = data["class_structure"]
            if "class_name" not in class_info:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message="Missing class name in architecture",
                    location="class_structure"
                ))
            elif not re.match(r'^[A-Z][a-zA-Z0-9]*$', class_info.get("class_name", "")):
                result.add_issue(ValidationIssue(
                    severity=Severity.WARNING,
                    message="Class name doesn't follow PascalCase convention",
                    location="class_structure.class_name",
                    suggestion="Use PascalCase for class names"
                ))
        
        # Validate interfaces
        if "interfaces" in data and isinstance(data["interfaces"], list):
            for idx, interface in enumerate(data["interfaces"]):
                if not interface.startswith("I"):
                    result.add_issue(ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"Interface '{interface}' doesn't follow naming convention",
                        location=f"interfaces[{idx}]",
                        suggestion="Interface names should start with 'I'"
                    ))


class TodoListValidator(BaseValidator):
    """Validates Step 5 output - implementation todo list."""
    
    def _validate_custom(self, data: Any, result: ValidationResult):
        """Validate todo list."""
        if not isinstance(data, dict) or "todos" not in data:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Todo list must contain 'todos' field"
            ))
            return
        
        todos = data["todos"]
        if not isinstance(todos, list):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Todos must be a list"
            ))
            return
        
        if len(todos) == 0:
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                message="Todo list is empty",
                suggestion="Add implementation tasks"
            ))
            return
        
        # Track categories
        categories = defaultdict(int)
        
        for idx, todo in enumerate(todos):
            location = f"todos[{idx}]"
            
            if not isinstance(todo, dict):
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Todo item {idx} must be a dictionary",
                    location=location
                ))
                continue
            
            # Check required fields
            required_fields = ["task", "category", "priority"]
            for field in required_fields:
                if field not in todo:
                    result.add_issue(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Todo item missing required field: {field}",
                        location=location,
                        field=field
                    ))
            
            # Validate priority
            if "priority" in todo:
                priority = todo["priority"]
                if priority not in ["HIGH", "MEDIUM", "LOW"]:
                    result.add_issue(ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"Invalid priority: {priority}",
                        location=location,
                        suggestion="Use HIGH, MEDIUM, or LOW"
                    ))
            
            # Track categories
            if "category" in todo:
                categories[todo["category"]] += 1
        
        # Check for essential categories
        essential_categories = ["registers", "initialization", "interfaces"]
        for category in essential_categories:
            if category not in categories:
                result.add_issue(ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"No todos for essential category: {category}",
                    suggestion=f"Add tasks for {category} implementation"
                ))


class CodeGenerationValidator(BaseValidator):
    """Validates Step 6 output - generated C# code."""
    
    def _validate_custom(self, data: Any, result: ValidationResult):
        """Validate generated C# code."""
        if not isinstance(data, dict) or "code" not in data:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Code generation output must contain 'code' field"
            ))
            return
        
        code = data["code"]
        if not isinstance(code, str):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Generated code must be a string"
            ))
            return
        
        # Basic syntax checks
        self._validate_csharp_syntax(code, result)
        
        # Renode-specific patterns
        self._validate_renode_patterns(code, result)
        
        # Code quality checks
        self._validate_code_quality(code, result)
    
    def _validate_csharp_syntax(self, code: str, result: ValidationResult):
        """Validate C# syntax basics."""
        # Check for balanced braces
        open_braces = code.count('{')
        close_braces = code.count('}')
        if open_braces != close_braces:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Unbalanced braces: {open_braces} open, {close_braces} close",
                suggestion="Check for missing opening or closing braces"
            ))
        
        # Check for namespace
        if not re.search(r'namespace\s+\w+', code):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Missing namespace declaration",
                suggestion="Add namespace declaration at the beginning"
            ))
        
        # Check for class definition
        if not re.search(r'public\s+class\s+\w+', code):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Missing public class definition",
                suggestion="Add public class for the peripheral"
            ))
        
        # Check for using statements
        if not re.search(r'using\s+', code):
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                message="No using statements found",
                suggestion="Add necessary using statements"
            ))
    
    def _validate_renode_patterns(self, code: str, result: ValidationResult):
        """Validate Renode-specific patterns."""
        required_patterns = [
            (r'IDoubleWordPeripheral|IWordPeripheral|IBytePeripheral', 
             "Missing peripheral interface implementation"),
            (r'RegistersCollection', "Missing RegistersCollection"),
            (r'DefineRegister', "Missing register definitions"),
            (r'\.Define\w*Register', "Missing register definition methods")
        ]
        
        for pattern, message in required_patterns:
            if not re.search(pattern, code):
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=message,
                    suggestion="Implement required Renode patterns"
                ))
        
        # Check for proper constructor
        if not re.search(r'public\s+\w+\s*\([^)]*Machine\s+machine', code):
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Constructor missing Machine parameter",
                suggestion="Add Machine parameter to constructor"
            ))
    
    def _validate_code_quality(self, code: str, result: ValidationResult):
        """Validate code quality aspects."""
        lines = code.split('\n')
        
        # Check for TODO comments
        todo_lines = [i for i, line in enumerate(lines, 1) if 'TODO' in line]
        if todo_lines:
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                message=f"Found {len(todo_lines)} TODO comments",
                suggestion="Complete TODO items before finalizing"
            ))
        
        # Check for proper documentation
        if not re.search(r'///', code):
            result.add_issue(ValidationIssue(
                severity=Severity.INFO,
                message="No XML documentation comments found",
                suggestion="Add XML documentation for public members"
            ))
        
        # Check line length
        long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 120]
        if long_lines:
            result.add_issue(ValidationIssue(
                severity=Severity.INFO,
                message=f"Found {len(long_lines)} lines exceeding 120 characters",
                suggestion="Consider breaking long lines for readability"
            ))


class ValidationEngine:
    """Main validation engine coordinating all validators."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize validation engine with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize step validators
        schema_dir = Path(config.get("schema_directory", "validation_schemas"))
        self.validators = {
            "section_summary": SectionSummaryValidator(schema_dir / "section_summary.json"),
            "data_extraction": DataExtractionValidator(schema_dir / "data_extraction.json"),
            "register_mapping": RegisterMappingValidator(schema_dir / "register_mapping.json"),
            "architecture": ArchitectureValidator(schema_dir / "architecture.json"),
            "todo_list": TodoListValidator(schema_dir / "todo_list.json"),
            "code_generation": CodeGenerationValidator(schema_dir / "code_generation.json")
        }
        
        # Validation history
        self.validation_history: List[Dict[str, Any]] = []
        
        # Cross-step data cache
        self.step_data_cache: Dict[str, Any] = {}
    
    def validate_step(self, step_name: str, data: Any) -> ValidationResult:
        """Validate a specific pipeline step."""
        if step_name not in self.validators:
            self.logger.error(f"Unknown step: {step_name}")
            result = ValidationResult(valid=False)
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Unknown validation step: {step_name}"
            ))
            return result
        
        # Cache step data for cross-validation
        self.step_data_cache[step_name] = data
        
        # Run step-specific validation
        validator = self.validators[step_name]
        result = validator.validate(data)
        result.metadata["step"] = step_name
        
        # Record validation
        self.validation_history.append({
            "step": step_name,
            "timestamp": result.timestamp,
            "result": result.to_dict()
        })
        
        self.logger.info(f"Validated {step_name}: valid={result.valid}, score={result.score:.1f}")
        
        return result
    
    def cross_validate_pipeline(self, pipeline_context: Dict[str, Any]) -> ValidationResult:
        """Perform cross-step validation across the entire pipeline."""
        result = ValidationResult()
        result.metadata["validation_type"] = "cross_step"
        
        # Update cache with pipeline context
        self.step_data_cache.update(pipeline_context)
        
        # Cross-validation checks
        self._validate_register_consistency(result)
        self._validate_architecture_register_match(result)
        self._validate_todo_coverage(result)
        self._validate_code_implementation_completeness(result)
        self._validate_peripheral_metadata_consistency(result)
        
        # Calculate final score
        result.calculate_score()
        
        # Record cross-validation
        self.validation_history.append({
            "step": "cross_validation",
            "timestamp": result.timestamp,
            "result": result.to_dict()
        })
        
        return result
    
    def _validate_register_consistency(self, result: ValidationResult):
        """Ensure register definitions are consistent across steps."""
        register_data = self.step_data_cache.get("register_mapping", {})
        arch_data = self.step_data_cache.get("architecture", {})
        
        if not register_data or not arch_data:
            return
        
        # Extract register names from different steps
        step3_registers = {r["name"] for r in register_data.get("registers", [])}
        
        # Check if architecture references all registers
        arch_registers = set()
        if "register_definitions" in arch_data:
            arch_registers = {r["name"] for r in arch_data["register_definitions"]}
        
        missing_in_arch = step3_registers - arch_registers
        if missing_in_arch:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Registers not referenced in architecture: {', '.join(missing_in_arch)}",
                suggestion="Update architecture to include all registers from Step 3"
            ))
        
        extra_in_arch = arch_registers - step3_registers
        if extra_in_arch:
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                message=f"Architecture references undefined registers: {', '.join(extra_in_arch)}",
                suggestion="Remove or define these registers in Step 3"
            ))
    
    def _validate_architecture_register_match(self, result: ValidationResult):
        """Validate that architecture properly defines all registers."""
        register_data = self.step_data_cache.get("register_mapping", {})
        code_data = self.step_data_cache.get("code_generation", {})
        
        if not register_data or not code_data:
            return
        
        registers = register_data.get("registers", [])
        code = code_data.get("code", "")
        
        # Check each register is implemented in code
        for register in registers:
            reg_name = register.get("name", "")
            if not re.search(rf'DefineRegister.*"{reg_name}"', code):
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Register '{reg_name}' not implemented in generated code",
                    suggestion=f"Add DefineRegister for '{reg_name}' in the implementation"
                ))
    
    def _validate_todo_coverage(self, result: ValidationResult):
        """Ensure todo list covers all necessary implementation tasks."""
        register_data = self.step_data_cache.get("register_mapping", {})
        todo_data = self.step_data_cache.get("todo_list", {})
        
        if not register_data or not todo_data:
            return
        
        registers = register_data.get("registers", [])
        todos = todo_data.get("todos", [])
        
        # Extract register-related todos
        register_todos = [t for t in todos if t.get("category") == "registers"]
        
        if len(register_todos) < len(registers):
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                message=f"Todo list has {len(register_todos)} register tasks but {len(registers)} registers defined",
                suggestion="Ensure each register has a corresponding implementation task"
            ))
        
        # Check for initialization todos
        init_todos = [t for t in todos if t.get("category") == "initialization"]
        if not init_todos:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="No initialization tasks in todo list",
                suggestion="Add initialization tasks for peripheral setup"
            ))
    
    def _validate_code_implementation_completeness(self, result: ValidationResult):
        """Validate that generated code implements all todo items."""
        todo_data = self.step_data_cache.get("todo_list", {})
        code_data = self.step_data_cache.get("code_generation", {})
        
        if not todo_data or not code_data:
            return
        
        todos = todo_data.get("todos", [])
        code = code_data.get("code", "")
        
        # Check high priority todos
        high_priority_todos = [t for t in todos if t.get("priority") == "HIGH"]
        
        for todo in high_priority_todos:
            task = todo.get("task", "")
            # Simple heuristic: check if key words from task appear in code
            keywords = re.findall(r'\b[A-Z][a-zA-Z]+\b', task)
            missing_keywords = [kw for kw in keywords if kw not in code]
            
            if len(missing_keywords) > len(keywords) / 2:
                result.add_issue(ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"High priority task may not be implemented: {task}",
                    suggestion="Verify implementation of all high priority tasks"
                ))
    
    def _validate_peripheral_metadata_consistency(self, result: ValidationResult):
        """Ensure peripheral metadata is consistent across all steps."""
        data_extraction = self.step_data_cache.get("data_extraction", {})
        architecture = self.step_data_cache.get("architecture", {})
        code_gen = self.step_data_cache.get("code_generation", {})
        
        if not data_extraction:
            return
        
        peripheral_name = data_extraction.get("peripheral_name", "")
        
        # Check architecture uses same peripheral name
        if architecture:
            arch_class = architecture.get("class_structure", {}).get("class_name", "")
            if peripheral_name and arch_class and peripheral_name not in arch_class:
                result.add_issue(ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Architecture class '{arch_class}' doesn't match peripheral name '{peripheral_name}'",
                    suggestion="Use consistent naming across all steps"
                ))
        
        # Check code uses same peripheral name
        if code_gen and peripheral_name:
            code = code_gen.get("code", "")
            if f"class {peripheral_name}" not in code and f"class {peripheral_name}Peripheral" not in code:
                result.add_issue(ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Generated code doesn't use peripheral name '{peripheral_name}'",
                    suggestion="Ensure generated class matches peripheral name"
                ))
    
    def validate_final_output(self, output_path: Union[str, Path]) -> ValidationResult:
        """Validate the final generated peripheral model file."""
        result = ValidationResult()
        result.metadata["validation_type"] = "final_output"
        
        output_path = Path(output_path)
        
        if not output_path.exists():
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Output file not found: {output_path}"
            ))
            return result
        
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Use code generation validator
            code_data = {"code": code}
            code_result = self.validators["code_generation"].validate(code_data)
            
            # Merge results
            result.issues.extend(code_result.issues)
            result.valid = code_result.valid
            result.score = code_result.score
            
            # Additional final checks
            self._validate_final_code_completeness(code, result)
            
        except Exception as e:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Error reading output file: {str(e)}"
            ))
        
        result.calculate_score()
        return result
    
    def _validate_final_code_completeness(self, code: str, result: ValidationResult):
        """Additional validation for final code completeness."""
        # Check for complete implementation (no stubs)
        if "throw new NotImplementedException" in code:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                message="Code contains NotImplementedException",
                suggestion="Implement all methods completely"
            ))
        
        # Check for proper error handling
        if "try" not in code and len(code) > 1000:
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                message="No error handling found in code",
                suggestion="Add try-catch blocks for error handling"
            ))
        
        # Check for logging
        if "this.Log" not in code and "Logger" not in code:
            result.add_issue(ValidationIssue(
                severity=Severity.INFO,
                message="No logging found in code",
                suggestion="Consider adding logging for debugging"
            ))
    
    def should_halt_pipeline(self, result: ValidationResult) -> bool:
        """Determine if pipeline should be halted based on validation result."""
        # Halt on any critical errors
        critical_errors = [i for i in result.issues if i.severity == Severity.ERROR]
        
        if critical_errors:
            self.logger.error(f"Pipeline halt recommended: {len(critical_errors)} critical errors found")
            return True
        
        # Halt if score is too low
        if result.score < self.config.get("min_validation_score", 60.0):
            self.logger.error(f"Pipeline halt recommended: score {result.score:.1f} below threshold")
            return True
        
        return False
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_validations": len(self.validation_history),
            "summary": {
                "total_errors": 0,
                "total_warnings": 0,
                "total_info": 0,
                "average_score": 0.0
            },
            "step_results": {},
            "cross_validation_results": None,
            "recommendations": []
        }
        
        # Aggregate statistics
        total_score = 0.0
        for validation in self.validation_history:
            result = validation["result"]
            step = validation["step"]
            
            report["summary"]["total_errors"] += result.get("error_count", 0)
            report["summary"]["total_warnings"] += result.get("warning_count", 0)
            report["summary"]["total_info"] += result.get("info_count", 0)
            total_score += result.get("score", 0)
            
            if step == "cross_validation":
                report["cross_validation_results"] = result
            else:
                report["step_results"][step] = result
        
        # Calculate average score
        if self.validation_history:
            report["summary"]["average_score"] = total_score / len(self.validation_history)
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on validation results."""
        recommendations = []
        
        # Check for critical issues
        if report["summary"]["total_errors"] > 0:
            recommendations.append(f"Fix {report['summary']['total_errors']} critical errors before proceeding")
        
        # Check for low scores
        if report["summary"]["average_score"] < 80:
            recommendations.append("Improve validation score by addressing warnings and errors")
        
        # Step-specific recommendations
        for step, result in report["step_results"].items():
            if not result.get("valid", True):
                recommendations.append(f"Review and fix issues in {step} step")
        
        # Cross-validation recommendations
        if report["cross_validation_results"] and not report["cross_validation_results"].get("valid", True):
            recommendations.append("Ensure consistency across all pipeline steps")
        
        return recommendations
    
    def export_report(self, filepath: Union[str, Path], format: str = "json") -> None:
        """Export validation report to file."""
        report = self.get_validation_report()
        filepath = Path(filepath)
        
        if format == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
        elif format == "html":
            html_content = self._generate_html_report(report)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        self.logger.info(f"Validation report exported to {filepath}")
    
    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML validation report."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Validation Report - {report['timestamp']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
        .error {{ color: #d32f2f; }}
        .warning {{ color: #f57c00; }}
        .info {{ color: #0288d1; }}
        .score {{ font-size: 24px; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .recommendation {{ background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>Validation Report</h1>
    <p>Generated: {report['timestamp']}</p>
    
    <div class="summary">
        <h2>Summary</h2>
        <p class="score">Average Score: {report['summary']['average_score']:.1f}/100</p>
        <p class="error">Errors: {report['summary']['total_errors']}</p>
        <p class="warning">Warnings: {report['summary']['total_warnings']}</p>
        <p class="info">Info: {report['summary']['total_info']}</p>
    </div>
    
    <h2>Recommendations</h2>
    {"".join(f'<div class="recommendation">{rec}</div>' for rec in report['recommendations'])}
    
    <h2>Step Results</h2>
    <table>
        <tr>
            <th>Step</th>
            <th>Valid</th>
            <th>Score</th>
            <th>Errors</th>
            <th>Warnings</th>
        </tr>
        {"".join(self._generate_step_row(step, result) for step, result in report['step_results'].items())}
    </table>
</body>
</html>
"""
        return html
    
    def _generate_step_row(self, step: str, result: Dict[str, Any]) -> str:
        """Generate HTML table row for a step result."""
        return f"""
        <tr>
            <td>{step}</td>
            <td>{'✓' if result.get('valid', False) else '✗'}</td>
            <td>{result.get('score', 0):.1f}</td>
            <td class="error">{result.get('error_count', 0)}</td>
            <td class="warning">{result.get('warning_count', 0)}</td>
        </tr>
        """


# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Example configuration
    config = {
        "schema_directory": "validation_schemas",
        "min_validation_score": 70.0
    }
    
    # Create validation engine
    engine = ValidationEngine(config)
    
    # Example: Validate register mapping
    register_data = {
        "registers": [
            {
                "name": "CONTROL_REG",
                "address": "0x00",
                "size": 32,
                "access": "RW",
                "reset_value": "0x00000000",
                "bit_fields": [
                    {
                        "name": "ENABLE",
                        "start_bit": 0,
                        "end_bit": 0,
                        "access": "RW"
                    },
                    {
                        "name": "MODE",
                        "start_bit": 1,
                        "end_bit": 3,
                        "access": "RW"
                    }
                ]
            }
        ]
    }
    
    result = engine.validate_step("register_mapping", register_data)
    print(f"Validation result: {result.to_dict()}")