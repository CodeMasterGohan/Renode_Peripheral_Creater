# Contributing to Renode Peripheral Model Generator

Thank you for your interest in contributing to the Renode Peripheral Model Generator! This guide will help you get started with contributing to the project.

## Table of Contents

- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting Guidelines](#issue-reporting-guidelines)
- [Development Workflow](#development-workflow)
- [Architecture Overview](#architecture-overview)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Docker (for Milvus)
- A code editor (VS Code recommended)

### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/renode-peripheral-generator.git
cd renode-peripheral-generator
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate
```

### Step 3: Install Development Dependencies

```bash
# Install in development mode
cd project
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Step 4: Set Up Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install
```

### Step 5: Configure Development Environment

```bash
# Copy environment template
cp .env.example .env.development

# Edit with your API keys
vim .env.development

# Set development mode
export ENVIRONMENT=development
```

### Step 6: Start Development Services

```bash
# Start Milvus for development
docker-compose -f docker-compose.dev.yml up -d

# Verify services
docker-compose -f docker-compose.dev.yml ps
```

## Code Style Guidelines

### Python Code Style

We follow PEP 8 with some modifications:

```python
# Good example
class PeripheralGenerator:
    """Generate Renode peripheral models from specifications."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the generator with configuration.

        Args:
            config: Configuration dictionary containing model settings
        """
        self.config = config
        self._validate_config()

    def generate_model(
        self,
        query: str,
        *,
        interactive: bool = False,
        output_dir: Optional[Path] = None
    ) -> GenerationResult:
        """Generate a peripheral model from a natural language query.

        Args:
            query: Natural language description of the peripheral
            interactive: Whether to run in interactive mode
            output_dir: Optional output directory override

        Returns:
            GenerationResult containing the generated code and metadata

        Raises:
            ValidationError: If the query is invalid
            GenerationError: If generation fails
        """
        # Implementation here
        pass
```

### Style Rules

1. **Line Length**: Maximum 100 characters (120 for comments with URLs)
2. **Imports**: Group in order: standard library, third-party, local
3. **Type Hints**: Use type hints for all public functions
4. **Docstrings**: Use Google-style docstrings
5. **Naming**:
   - Classes: `PascalCase`
   - Functions/variables: `snake_case`
   - Constants: `UPPER_SNAKE_CASE`
   - Private: prefix with `_`

### C# Code Style (Generated Code)

```csharp
// Follow Renode conventions
namespace Antmicro.Renode.Peripherals.DMA
{
    public class DMAController : BasicDoubleWordPeripheral, IDMA
    {
        public DMAController(Machine machine, int numberOfChannels = 64)
            : base(machine)
        {
            this.numberOfChannels = numberOfChannels;
            channels = new Channel[numberOfChannels];
            DefineRegisters();
        }

        private void DefineRegisters()
        {
            // Register definitions
        }

        private readonly int numberOfChannels;
        private readonly Channel[] channels;
    }
}
```

### Commit Message Format

```
type(scope): subject

body

footer
```

Examples:

```
feat(pipeline): add parallel processing support

- Implement parallel task execution in generation pipeline
- Add configuration for max workers
- Include progress tracking for parallel tasks

Closes #123
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

## Testing Requirements

### Unit Tests

All new code must include unit tests:

```python
# test_model_manager.py
import pytest
from model_manager import ModelManager

class TestModelManager:
    @pytest.fixture
    def manager(self):
        config = {"default_provider": "openai"}
        return ModelManager(config)

    def test_model_selection(self, manager):
        """Test model selection for different tasks."""
        assert manager.select_model("analysis") == "gpt-4"
        assert manager.select_model("code_generation") == "claude-3-opus"

    def test_generate_with_retry(self, manager, mocker):
        """Test generation with retry logic."""
        mock_generate = mocker.patch.object(manager, '_generate')
        mock_generate.side_effect = [Exception("API Error"), "Success"]

        result = manager.generate("test prompt", max_retries=2)
        assert result == "Success"
        assert mock_generate.call_count == 2
```

### Integration Tests

```python
# test_integration.py
import pytest
from pathlib import Path

@pytest.mark.integration
class TestPeripheralGeneration:
    def test_gpio_generation(self, app):
        """Test end-to-end GPIO generation."""
        result = app.generate(
            "Create a simple GPIO controller",
            output_dir=Path("test_output")
        )

        assert result.success
        assert result.validation_score >= 80
        assert Path(result.output_file).exists()
```

### Test Coverage

- Minimum coverage: 80%
- Critical paths: 95%
- Run coverage: `pytest --cov=. --cov-report=html`

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes

- Write code following style guidelines
- Add/update tests
- Update documentation
- Add changelog entry

### 3. Run Tests Locally

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_model_manager.py

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

### 4. Run Linting

```bash
# Run all linters
pre-commit run --all-files

# Or individually:
black .
isort .
flake8 .
mypy .
```

### 5. Create Pull Request

1. Push your branch: `git push origin feature/your-feature-name`
2. Open PR on GitHub
3. Fill out PR template
4. Link related issues
5. Request review

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Changelog updated
```

### Review Process

1. Automated checks must pass
2. At least one maintainer approval required
3. All conversations resolved
4. Branch up to date with main

## Issue Reporting Guidelines

### Bug Reports

Use the bug report template:

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**

1. Run command '...'
2. See error

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Environment:**

- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.5]
- Project version: [e.g., 1.0.0]

**Additional context**
Any other relevant information

**Logs**
```

Relevant log output

```

```

### Feature Requests

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution**
Your proposed solution

**Alternatives considered**
Other solutions you've considered

**Additional context**
Any other information
```

## Development Workflow

### 1. Daily Development

```bash
# Start your day
git pull origin main
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Test changes
pytest tests/

# Commit
git add .
git commit -m "feat: add new feature"

# Push
git push origin feature/new-feature
```

### 2. Debugging

```python
# Use debug configuration
# config.yaml
development:
  debug: true
  save_intermediates: true

# Add debug logging
import logging
logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Processing data: {data}")
    # ... processing ...
    logger.debug(f"Result: {result}")
    return result
```

### 3. Performance Profiling

```python
# Profile code
import cProfile
import pstats

def profile_generation():
    profiler = cProfile.Profile()
    profiler.enable()

    # Run generation
    generator.generate("Create GPIO controller")

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

## Architecture Overview

### Component Structure

```
project/
├── core/
│   ├── __init__.py
│   ├── base.py              # Base classes
│   └── exceptions.py        # Custom exceptions
├── handlers/
│   ├── milvus_handler.py    # Vector DB operations
│   └── llm_handler.py       # LLM interactions
├── pipeline/
│   ├── stages/              # Pipeline stages
│   └── orchestrator.py      # Pipeline orchestration
├── validation/
│   ├── validators.py        # Validation logic
│   └── schemas/             # Validation schemas
└── utils/
    ├── config.py            # Configuration management
    └── helpers.py           # Utility functions
```

### Adding New Features

1. **New LLM Provider**:

   ```python
   # handlers/providers/newllm.py
   class NewLLMProvider(BaseLLMProvider):
       def generate(self, prompt: str, **kwargs) -> str:
           # Implementation
           pass
   ```

2. **New Validation Rule**:

   ```python
   # validation/rules/custom_rule.py
   class CustomRule(BaseValidationRule):
       def validate(self, code: str) -> ValidationResult:
           # Implementation
           pass
   ```

3. **New Pipeline Stage**:
   ```python
   # pipeline/stages/custom_stage.py
   class CustomStage(BasePipelineStage):
       def execute(self, context: PipelineContext) -> StageResult:
           # Implementation
           pass
   ```

### Database Schema

```sql
-- Milvus collections
CREATE COLLECTION peripheral_docs (
    id VARCHAR PRIMARY KEY,
    content TEXT,
    embedding FLOAT_VECTOR[384],
    metadata JSON
);

CREATE COLLECTION code_examples (
    id VARCHAR PRIMARY KEY,
    code TEXT,
    embedding FLOAT_VECTOR[384],
    peripheral_type VARCHAR,
    metadata JSON
);
```

## Best Practices

### 1. Error Handling

```python
# Good
try:
    result = llm.generate(prompt)
except APIError as e:
    logger.error(f"API error: {e}")
    raise GenerationError(f"Failed to generate: {e}") from e
except Exception as e:
    logger.exception("Unexpected error")
    raise

# Bad
try:
    result = llm.generate(prompt)
except:
    pass  # Never silent fail
```

### 2. Configuration Management

```python
# Good
class Config:
    def __init__(self, config_path: Path):
        self._config = self._load_config(config_path)
        self._validate_config()

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation."""
        # config.get("models.openai.api_key")
        pass

# Bad
config = yaml.load(open("config.yaml"))  # Direct global access
```

### 3. Testing Practices

```python
# Good - Isolated, mockable
def test_generation(mocker):
    mock_llm = mocker.Mock()
    mock_llm.generate.return_value = "generated code"

    generator = Generator(llm=mock_llm)
    result = generator.generate("query")

    assert "generated code" in result

# Bad - External dependencies
def test_generation():
    generator = Generator()  # Uses real LLM
    result = generator.generate("query")
    assert result  # Flaky, expensive
```

## Resources

### Documentation

- [Renode Documentation](https://docs.renode.io/)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### Tools

- [Black](https://black.readthedocs.io/) - Code formatter
- [isort](https://pycqa.github.io/isort/) - Import sorter
- [mypy](http://mypy-lang.org/) - Type checker
- [pytest](https://docs.pytest.org/) - Testing framework

### Community

- GitHub Discussions for questions
- GitHub Issues for bugs/features
- Discord/Slack for real-time chat (if available)

## Getting Help

If you need help:

1. Check existing documentation
2. Search closed issues
3. Ask in discussions
4. Create an issue with details

Thank you for contributing to make Renode Peripheral Model Generator better!
