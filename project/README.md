# Renode Peripheral Generator

This project generates Renode peripheral models from documentation using a multi-step LLM pipeline.

## Features

- **Batch Document Processing**: Convert Markdown documentation into RAG-ready JSON chunks
- **Peripheral Model Generation**: Multi-step LLM pipeline to generate Renode peripheral models
- **Validation**: Schema validation at each pipeline stage
- **Error Handling**: Robust error handling and retry mechanisms

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Batch Processing Documentation
Process all Markdown files in the docs directory and ingest into Milvus:
```bash
python batch_chunk_processor.py --input-dir ../docs --output-dir chunks
```

The pipeline will:
1. Convert each Markdown file into JSON chunks
2. Save chunks to the output directory
3. Ingest chunks into Milvus for vector search

> **Note**: Chunks must include these metadata fields:
> - `source_file`
> - `chapter_title`
> - `heading_hierarchy`
> - `chunk_type`
> - `peripheral_name`
> - `section_type`

### Generating a Peripheral Model
Run the generation pipeline for a specific peripheral:
```bash
python generation_pipeline.py --peripheral "UART" --documentation "path/to/documentation.md"
```

## Project Structure
- `batch_chunk_processor.py`: Batch processes Markdown files and ingests chunks into Milvus
- `generation_pipeline.py`: Main peripheral generation pipeline
- `chunk_processor.py`: Processes individual Markdown files
- `model_manager.py`: Manages LLM interactions
- `validation_engine.py`: Validates pipeline outputs
- `milvus_rag_handler.py`: Handles vector storage and retrieval
- `schemas/`: JSON validation schemas
- `templates/`: Renode peripheral templates
- `chunks/`: Output directory for processed chunks

## Configuration
Edit `config.yaml` to customize model selection, validation thresholds, and pipeline parameters.