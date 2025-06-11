import argparse
import os
import json
import logging
from milvus_rag_handler import MilvusRAGHandler
from tqdm import tqdm
from chunk_processor import process_markdown_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_directory(input_dir: str, output_dir: str) -> None:
    """Process all markdown files in input directory and save chunks to output directory."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all markdown files in input directory
    md_files = [
        f for f in os.listdir(input_dir) 
        if f.endswith('.md') and os.path.isfile(os.path.join(input_dir, f))
    ]
    md_files.sort()  # Process in filename order
    
    logger.info(f"Found {len(md_files)} Markdown files to process")
    
    # Process each file with progress bar
    for filename in tqdm(md_files, desc="Processing chapters"):
        file_path = os.path.join(input_dir, filename)
        output_file = os.path.join(
            output_dir, 
            f"{filename.split('-')[0]}_chunks.json"  # Use chapter number prefix
        )
        
        try:
            logger.info(f"Processing {filename}")
            chunks = process_markdown_file(file_path)
            
            # Save chunks to JSON file
            with open(output_file, 'w') as f:
                json.dump(chunks, f, indent=2)
            logger.info(f"Saved chunks to {output_file}")
            
            # Ingest into Milvus
            try:
                handler = MilvusRAGHandler()
                handler.update_knowledge_base(knowledge_dir=output_dir)
                logger.info(f"Ingested chunks for {filename} into Milvus")
            except Exception as e:
                logger.error(f"Milvus ingestion failed for {filename}: {str(e)}")
                # Create error placeholder for Milvus failure
                error_file = output_file.replace('.json', '_milvus_error.txt')
                with open(error_file, 'w') as f:
                    f.write(f"Milvus ingestion error: {str(e)}")
                logger.info(f"Created Milvus error placeholder at {error_file}")
                
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")
            # Create error placeholder file
            with open(output_file, 'w') as f:
                json.dump({"error": str(e)}, f)
            logger.info(f"Created error placeholder at {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Batch process Markdown files into RAG-ready JSON chunks'
    )
    parser.add_argument('--input-dir', 
                        default='../docs',
                        help='Input directory containing Markdown files')
    parser.add_argument('--output-dir', 
                        default='chunks',
                        help='Output directory for JSON chunks')
    
    args = parser.parse_args()
    
    logger.info(f"Starting batch processing")
    logger.info(f"Input directory: {args.input_dir}")
    logger.info(f"Output directory: {args.output_dir}")
    
    process_directory(args.input_dir, args.output_dir)
    logger.info("Batch processing completed")