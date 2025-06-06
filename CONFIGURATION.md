# Configuration Guide

This document provides a comprehensive reference for configuring the Renode Peripheral Model Generator.

## Table of Contents

- [Configuration File Structure](#configuration-file-structure)
- [Environment Variables](#environment-variables)
- [Milvus Configuration](#milvus-configuration)
- [LLM Provider Configuration](#llm-provider-configuration)
- [Validation Settings](#validation-settings)
- [Pipeline Parameters](#pipeline-parameters)
- [Advanced Configuration](#advanced-configuration)

## Configuration File Structure

The main configuration file is `config.yaml` located in the project directory. It uses YAML format and is organized into logical sections.

### Basic Structure

```yaml
# Main sections
milvus: # Vector database configuration
models: # LLM provider settings
validation: # Code validation rules
todo: # TODO processing configuration
templates: # Template settings
output: # Output file organization
pipeline: # Generation pipeline settings
logging: # Logging configuration
knowledge_base: # Knowledge base management
accuracy: # Accuracy tracking
development: # Development settings
cache: # Caching configuration
integrations: # External integrations
security: # Security settings
```

## Environment Variables

Environment variables can override configuration file settings. Create a `.env` file based on `.env.example`:

### Required Variables

```env
# LLM API Keys (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Milvus Connection
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### Optional Variables

```env
# Milvus Authentication
MILVUS_USER=admin
MILVUS_PASSWORD=password

# Local LLM Support
LOCAL_LLM_ENDPOINT=http://localhost:8080
LOCAL_LLM_API_KEY=local-key

# Development Settings
DEBUG_MODE=true
DRY_RUN=false
LOG_LEVEL=DEBUG

# Performance Settings
MAX_CONCURRENT_REQUESTS=5
REQUEST_TIMEOUT=120
ENABLE_CACHE=true
```

## Milvus Configuration

Configure the Milvus vector database for documentation retrieval:

### Basic Settings

```yaml
milvus:
  host: "localhost" # Milvus server host
  port: 19530 # Milvus server port
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
  embedding_dim: 384 # Must match embedding model output
```

### Collection Configuration

```yaml
milvus:
  collections:
    peripheral_docs: "peripheral_documentation"
    renode_examples: "renode_code_examples"
```

### Index Parameters

```yaml
milvus:
  index_params:
    metric_type: "L2" # L2, IP, COSINE
    index_type: "IVF_FLAT" # IVF_FLAT, IVF_SQ8, IVF_PQ
    nlist: 128 # Number of clusters
```

### Advanced Milvus Settings

```yaml
milvus:
  search_params:
    nprobe: 10 # Number of clusters to search
  connection_params:
    timeout: 30 # Connection timeout in seconds
    keepalive: true
  pool_size: 10 # Connection pool size
```

## LLM Provider Configuration

Configure multiple LLM providers for different tasks:

### API Keys

```yaml
models:
  openai_api_key: "${OPENAI_API_KEY}"
  anthropic_api_key: "${ANTHROPIC_API_KEY}"
```

### Model Selection

```yaml
models:
  preferences:
    analysis: "gpt-4" # Best for understanding requirements
    code_generation: "claude-3-opus" # Best for code generation
    testing: "gpt-4" # Best for test generation
    documentation: "gpt-4-turbo" # Fast documentation generation
```

### Model-Specific Parameters

```yaml
models:
  temperature_defaults:
    analysis: 0.3 # Lower = more focused
    code_generation: 0.1 # Very low for consistent code
    testing: 0.5 # Medium for diverse tests
    documentation: 0.7 # Higher for natural text

  max_tokens:
    default: 4096
    code_generation: 8192 # More tokens for complex code
    documentation: 6000
```

### Provider Configuration

```yaml
models:
  providers:
    openai:
      base_url: "https://api.openai.com/v1"
      organization: "org-..." # Optional
      retry_attempts: 3

    anthropic:
      base_url: "https://api.anthropic.com/v1"
      version: "2023-06-01"
      retry_attempts: 3
```

## Validation Settings

Configure code validation rules and thresholds:

### Basic Validation

```yaml
validation:
  schema_directory: "validation_schemas"
  strict_mode: true # Fail on any validation error
```

### Validation Thresholds

```yaml
validation:
  thresholds:
    min_test_coverage: 80 # Minimum test coverage percentage
    max_complexity_score: 50 # Maximum cyclomatic complexity
    min_documentation_score: 70 # Minimum documentation completeness
```

### Code Quality Checks

```yaml
validation:
  code_quality:
    check_naming_conventions: true
    check_renode_patterns: true
    check_error_handling: true
    check_logging: true
    check_memory_safety: true
    check_thread_safety: false # Optional for single-threaded peripherals
```

### Custom Validation Rules

```yaml
validation:
  custom_rules:
    - name: "register_alignment"
      pattern: "Register\\s+\\w+\\s*=\\s*0x[0-9A-F]+"
      message: "Registers must be 4-byte aligned"

    - name: "interrupt_handling"
      required_methods: ["OnGPIO", "Reset"]
      message: "Interrupt peripherals must implement required methods"
```

## Pipeline Parameters

Configure the generation pipeline behavior:

### Step Configuration

```yaml
pipeline:
  steps:
    - name: "context_gathering"
      enabled: true
      timeout: 60
      retries: 3

    - name: "todo_generation"
      enabled: true
      timeout: 45
      retries: 2

    - name: "implementation"
      enabled: true
      timeout: 120
      retries: 3
```

### Timeout Settings

```yaml
pipeline:
  timeouts:
    context_gathering: 60 # Seconds
    todo_generation: 45
    interface_definition: 60
    implementation: 120
    test_generation: 90
    final_assembly: 30
```

### Retry Configuration

```yaml
pipeline:
  retry:
    max_attempts: 3
    backoff_multiplier: 2 # Exponential backoff
    initial_delay: 5 # Seconds
    max_delay: 60 # Maximum retry delay
```

### Parallel Execution

```yaml
pipeline:
  parallel:
    enabled: false # Enable parallel processing
    max_workers: 4 # Maximum parallel tasks
    task_timeout: 300 # Individual task timeout
```

## Advanced Configuration

### Caching

```yaml
cache:
  response_cache:
    enabled: true
    max_size: 1000 # Number of cached responses
    ttl: 3600 # Time to live in seconds

  embedding_cache:
    enabled: true
    directory: "cache/embeddings"
    max_size: "1GB"
    compression: true
```

### Logging

```yaml
logging:
  level: "INFO" # DEBUG, INFO, WARNING, ERROR

  file:
    enabled: true
    path: "logs/generator.log"
    max_size: "10MB"
    backup_count: 5
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

  console:
    enabled: true
    colored: true
    format: "%(levelname)s: %(message)s"

  performance:
    log_llm_calls: true
    log_token_usage: true
    log_response_times: true
```

### Knowledge Base

```yaml
knowledge_base:
  renode_knowledge_dir: "renode_knowledge"

  auto_update:
    enabled: true
    check_interval: 86400 # 24 hours
    sources:
      - url: "https://github.com/renode/renode"
        type: "git"
        paths: ["src/Infrastructure/src/Emulator/Peripherals"]

  indexing:
    chunk_size: 1000
    chunk_overlap: 200
    metadata_extraction: true
    embedding_batch_size: 32
```

### Security

```yaml
security:
  encrypt_api_keys: false # Use system keyring

  validate_inputs: true
  max_input_length: 100000 # Maximum query length
  allowed_file_types: [".cs", ".txt", ".md", ".json"]

  sanitize_outputs: true
  remove_sensitive_data: true
  sensitive_patterns:
    - "api[_-]?key"
    - "password"
    - "secret"
```

### Development Settings

```yaml
development:
  debug: false
  dry_run: false # Skip actual generation

  save_intermediates: true
  intermediates_dir: "debug/intermediates"

  profiling:
    enabled: false
    output_file: "debug/profile.stats"

  mock_llm_responses: false # Use mock responses for testing
  mock_response_dir: "tests/mock_responses"
```

## Configuration Precedence

Configuration values are resolved in the following order (highest to lowest precedence):

1. Command-line arguments
2. Environment variables
3. `.env` file
4. `config.yaml` file
5. Default values

## Configuration Validation

The system validates configuration on startup. Common validation errors:

### Missing Required Fields

```
Error: Missing required configuration field: models.openai_api_key
Solution: Add OPENAI_API_KEY to your .env file
```

### Invalid Values

```
Error: Invalid value for pipeline.timeouts.implementation: -1
Solution: Timeout values must be positive integers
```

### Type Mismatches

```
Error: Expected integer for milvus.port, got string: "19530"
Solution: Remove quotes from numeric values in YAML
```

## Best Practices

1. **Use Environment Variables for Secrets**

   - Never commit API keys to version control
   - Use `.env` file for local development
   - Use system environment variables in production

2. **Start with Defaults**

   - The default configuration works for most use cases
   - Only modify settings you understand
   - Test changes incrementally

3. **Monitor Performance**

   - Enable performance logging to identify bottlenecks
   - Adjust timeouts based on your system capabilities
   - Use caching to improve response times

4. **Validate Changes**
   - Run `python main.py test-connection` after configuration changes
   - Check logs for configuration warnings
   - Use `--dry-run` to test without consuming API credits

## Troubleshooting Configuration Issues

### Debug Configuration Loading

```bash
# Show resolved configuration
python main.py show-config

# Validate configuration
python main.py validate-config
```

### Common Issues

1. **Environment Variable Not Loading**

   ```bash
   # Check if .env file is in correct location
   ls -la project/.env

   # Verify variable is set
   echo $OPENAI_API_KEY
   ```

2. **YAML Syntax Errors**

   ```bash
   # Validate YAML syntax
   python -c "import yaml; yaml.safe_load(open('config.yaml'))"
   ```

3. **Permission Issues**
   ```bash
   # Check file permissions
   chmod 600 .env  # Restrict .env file access
   chmod 644 config.yaml
   ```

## Configuration Examples

### Minimal Configuration

```yaml
# Minimum required configuration
milvus:
  host: "localhost"
  port: 19530

models:
  openai_api_key: "${OPENAI_API_KEY}"
```

### Production Configuration

```yaml
# Production-ready configuration
milvus:
  host: "milvus.production.internal"
  port: 19530
  connection_params:
    timeout: 60
    keepalive: true

models:
  preferences:
    analysis: "gpt-4"
    code_generation: "claude-3-opus"

validation:
  strict_mode: true
  thresholds:
    min_test_coverage: 90

logging:
  level: "WARNING"
  file:
    enabled: true
    path: "/var/log/renode-generator/app.log"

cache:
  response_cache:
    enabled: true
    max_size: 5000

security:
  encrypt_api_keys: true
  validate_inputs: true
```

### Development Configuration

```yaml
# Development configuration with debugging
development:
  debug: true
  save_intermediates: true

logging:
  level: "DEBUG"
  console:
    colored: true

pipeline:
  retry:
    max_attempts: 1 # Fail fast in development

cache:
  response_cache:
    enabled: false # Disable cache for testing
```
