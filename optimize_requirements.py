import re
import sys
from stdlib_list import stdlib_list

# Import to package mapping
IMPORT_TO_PACKAGE = {
    "dotenv": "python-dotenv",
    "yaml": "pyyaml",
    "tiktoken": "tiktoken",
    "anthropic": "anthropic",
    "openai": "openai",
    "httpx": "httpx",
    "jsonschema": "jsonschema",
    "rich": "rich",
    "tenacity": "tenacity",
    "sklearn": "scikit-learn",
    "PIL": "Pillow",
    "dateutil": "python-dateutil",
    "bs4": "beautifulsoup4"
}

# Core dependencies to preserve
CORE_DEPENDENCIES = {"milvus", "pymilvus", "pyyaml", "python-dotenv", "tiktoken"}

# Dev package identifiers
DEV_KEYWORDS = {"test", "pytest", "coverage", "flake8", "mypy", "black", "isort", "sphinx"}

# Redundant packages (key: redundant, value: preferred)
REDUNDANT_PACKAGES = {"ruamel.yaml": "pyyaml"}

def extract_imports(file_paths):
    """Extract imports from Python files"""
    import_pattern = r'^\s*(?:import|from)\s+(\w+)'
    imports = set()
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                matches = re.findall(import_pattern, content, re.MULTILINE)
                imports.update(matches)
        except FileNotFoundError:
            print(f"Warning: File not found - {file_path}", file=sys.stderr)
    
    return imports

def map_imports_to_packages(imports):
    """Map import names to package names"""
    packages = set()
    stdlib = set(stdlib_list("3.8"))
    
    for imp in imports:
        # Skip standard library modules
        if imp in stdlib:
            continue
            
        # Handle special mappings
        package = IMPORT_TO_PACKAGE.get(imp, imp)
        
        # Skip local modules (no dot in package name)
        if '.' not in package:
            packages.add(package.lower())
    
    return packages

def parse_requirements(requirements_path):
    """Parse requirements.txt into package-version pairs"""
    requirements = {}
    with open(requirements_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Handle package specifications
            if '==' in line:
                pkg, version = line.split('==', 1)
                requirements[pkg.lower()] = version.strip()
            else:
                # Handle other formats
                pkg = re.split(r'[<>=]', line)[0].strip()
                requirements[pkg.lower()] = ""
    
    return requirements

def is_dev_package(package):
    """Check if package is development-only"""
    return any(keyword in package for keyword in DEV_KEYWORDS)

def optimize_requirements(import_packages, requirements):
    """Apply optimization rules to requirements"""
    optimized = {}
    
    for pkg, version in requirements.items():
        pkg_lower = pkg.lower()
        
        # Preserve core dependencies
        if pkg_lower in CORE_DEPENDENCIES:
            optimized[pkg] = version
            continue
            
        # Remove dev packages
        if is_dev_package(pkg_lower):
            continue
            
        # Remove redundant packages
        if pkg_lower in REDUNDANT_PACKAGES:
            preferred = REDUNDANT_PACKAGES[pkg_lower]
            if preferred in requirements or preferred in import_packages:
                continue
                
        # Keep packages with import references
        if pkg_lower in import_packages:
            optimized[pkg] = version
            
    return optimized

def main():
    # Files to process
    python_files = [
        'project/generation_pipeline.py',
        'project/main.py',
        'project/renode_templates.py',
        'project/todo_processor.py',
        'project/validation_engine.py',
        'project/model_manager.py'
    ]
    
    # Extract and map imports
    imports = extract_imports(python_files)
    import_packages = map_imports_to_packages(imports)
    
    # Parse requirements
    requirements = parse_requirements('project/requirements.txt')
    
    # Optimize requirements
    optimized_reqs = optimize_requirements(import_packages, requirements)
    
    # Generate new requirements.txt content
    output = ["# Optimized Renode Peripheral Model Generator Requirements\n"]
    for pkg, version in optimized_reqs.items():
        if version:
            output.append(f"{pkg}=={version}")
        else:
            output.append(pkg)
    
    # Write optimized requirements
    with open('project/optimized_requirements.txt', 'w') as f:
        f.write('\n'.join(output))
    
    print("Optimized requirements written to project/optimized_requirements.txt")

if __name__ == "__main__":
    main()