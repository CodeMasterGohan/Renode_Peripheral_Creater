# Renode Peripheral Model Generator

A sophisticated AI-powered tool for automatically generating high-quality Renode peripheral models from natural language descriptions and technical documentation.

## 🚀 Overview

The Renode Peripheral Model Generator leverages state-of-the-art RAG (Retrieval-Augmented Generation) technology combined with multiple LLMs to create accurate, validated, and production-ready Renode peripheral models. It transforms complex technical documentation into working C# code that integrates seamlessly with the Renode emulation framework.

### Key Features

- **Multi-LLM Pipeline**: Intelligently routes tasks to specialized models (GPT-4, Claude-3) for optimal results
- **RAG-Based Documentation Retrieval**: Uses Milvus vector database to find relevant technical documentation
- **Comprehensive Validation**: Multi-stage validation ensures generated code meets Renode standards
- **Interactive Generation**: Step-by-step generation with user confirmation at each stage
- **TODO Processing**: Automatically completes implementation TODOs using context-aware AI
- **Template Library**: Pre-built templates for common peripheral types (UART, GPIO, Timer, etc.)

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        User Interface (CLI)                         │
├─────────────────────────────────────────────────────────────────────┤
│                      Main Application (main.py)                     │
├─────────────────────────────────────────────────────────────────────┤
│                         Core Components                             │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │ Milvus RAG      │  │ Model Manager    │  │ Validation      │  │
│  │ Handler         │  │ (Multi-LLM)      │  │ Engine          │  │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘  │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │ Generation      │  │ TODO Processor   │  │ Renode          │  │
│  │ Pipeline        │  │                  │  │ Templates       │  │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│                      External Services                              │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │ Milvus Vector   │  │ OpenAI API       │  │ Anthropic API   │  │
│  │ Database        │  │                  │  │                 │  │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Milvus vector database (local or cloud instance)
- API keys for OpenAI and/or Anthropic

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/renode-peripheral-generator.git
cd renode-peripheral-generator
```

### Step 2: Install Dependencies

```bash
pip install -r project/requirements.txt
```

### Step 3: Configure Environment

1. Copy the example environment file:

   ```bash
   cp project/.env.example project/.env
   ```

2. Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   MILVUS_HOST=localhost
   MILVUS_PORT=19530
   ```

### Step 4: Configure OpenRouter (Optional)

To use OpenRouter as an alternative LLM provider:

1. Get an API key from [OpenRouter](https://openrouter.ai/)
2. Add to `.env`:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
3. Configure model preferences in `config.yaml`:
   ```yaml
   models:
     preferences:
       analysis: "openrouter/anthropic/claude-3-opus"
       code_generation: "openrouter/meta-llama/llama-3-70b-instruct"
   ```

### Step 5: Start Milvus (if running locally)

```bash
# Using Docker
docker-compose up -d milvus
```

### Step 6: Initialize the Knowledge Base

```bash
cd project
python main.py test-connection
```

## 🚀 Quick Start

### Generate a Simple GPIO Peripheral

```bash
python main.py generate "Create a Renode model for a GPIO controller with 32 pins"
```

### Interactive Mode

```bash
python main.py generate --interactive
```

### Validate an Existing Model

```bash
python main.py validate path/to/peripheral.cs --fix
```

## 📖 Usage Examples

### Example 1: Generate an eDMA Controller

```bash
python main.py generate "Create a Renode model for the MPC5554 eDMA controller with 64 channels"
```

This will:

1. Search relevant documentation in the vector database
2. Generate a comprehensive peripheral model
3. Validate the generated code
4. Create integration instructions

### Example 2: Generate from Specific Documentation

```bash
python main.py generate "Create a UART peripheral based on chapter 20 of the MPC5554 reference manual" --interactive
```

### Example 3: Export Templates

```bash
python main.py export-templates --output ./my-templates
```

## ⚙️ Configuration

The system is configured through `config.yaml`. Key configuration sections include:

### LLM Configuration

```yaml
models:
  preferences:
    analysis: "gpt-4"
    code_generation: "claude-3-opus"
    testing: "gpt-4"
    documentation: "gpt-4-turbo"
```

### Validation Settings

```yaml
validation:
  thresholds:
    min_test_coverage: 80
    max_complexity_score: 50
    min_documentation_score: 70
```

### Pipeline Configuration

```yaml
pipeline:
  timeouts:
    context_gathering: 60
    implementation: 120
  retry:
    max_attempts: 3
```

See [CONFIGURATION.md](CONFIGURATION.md) for detailed configuration reference.

## 🔧 Troubleshooting

### Common Issues

1. **Milvus Connection Failed**

   - Ensure Milvus is running: `docker ps | grep milvus`
   - Check connection settings in `.env`
   - Verify firewall settings

2. **API Key Errors**

   - Verify API keys are correctly set in `.env`
   - Check API key permissions and quotas
   - Try using a different LLM provider

3. **OpenRouter Specific Issues**

   - Ensure `OPENROUTER_API_KEY` is set in `.env`
   - Verify model names in `config.yaml` match OpenRouter's model list
   - Check OpenRouter status page for outages
   - Some models may require accepting terms on OpenRouter website

4. **Generation Timeouts**

   - Increase timeout values in `config.yaml`
   - Simplify your query
   - Use `--interactive` mode for step-by-step generation

4. **Validation Failures**
   - Review the validation report
   - Use `--fix` flag to attempt automatic fixes
   - Check generated code against Renode patterns

### Debug Mode

Enable debug mode for detailed logging:

```bash
export DEBUG_MODE=true
python main.py generate "your query"
```

### Getting Help

- Check the [Examples](EXAMPLES.md) for detailed tutorials
- Review [Configuration](CONFIGURATION.md) for advanced settings
- Submit issues on GitHub with debug logs

## 📚 Documentation

- [Configuration Guide](CONFIGURATION.md) - Detailed configuration reference
- [Examples & Tutorials](EXAMPLES.md) - Step-by-step tutorials and examples
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project
- [Architecture Overview](ARCHITECTURE.md) - Technical architecture details

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up a development environment
- Code style guidelines
- Submitting pull requests
- Reporting issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Renode](https://renode.io/) - The open-source hardware emulation framework
- [Milvus](https://milvus.io/) - Vector database for similarity search
- [OpenAI](https://openai.com/) & [Anthropic](https://anthropic.com/) - LLM providers
- [OpenRouter](https://openrouter.ai/) - Unified API for multiple LLMs

## OpenRouter Usage Examples

### Example: Using OpenRouter Models

```bash
# Generate with specific OpenRouter model
python main.py generate "Create timer peripheral" --model openrouter/anthropic/claude-3-opus
```

### Example: Comparing Models

```bash
# Compare outputs from different providers
python main.py generate "Create UART peripheral" --compare openrouter/anthropic/claude-3-opus openrouter/meta-llama/llama-3-70b-instruct
```

## 📞 Support

- **Documentation**: See the `/docs` folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/renode-peripheral-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/renode-peripheral-generator/discussions)
