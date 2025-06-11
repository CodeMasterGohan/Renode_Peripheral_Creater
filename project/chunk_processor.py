import re
import json
from slugify import slugify
from jsonschema import validate
from typing import List, Dict, Tuple

# Constants
TABLE_PATTERN = r'(\|.*\|\n)(?:\| *:?[-]+:? *\|)+\n((?:\|.*\|\n?)+)'
HEADING_PATTERN = r'^(#+)\s+(.*)$'
REGISTER_DIAGRAM_PATTERN = re.compile(
    r'Figure\s+\d+-\d+\..*?register', 
    re.IGNORECASE
)
LIST_PATTERN = re.compile(r'^(\s*[-*+] .+|\s*\d+\. .+)', re.MULTILINE)

# JSON schema for output validation
CHUNK_SCHEMA = {
    "type": "object",
    "properties": {
        "chunk_id": {"type": "string"},
        "source_file": {"type": "string"},
        "chapter_title": {"type": "string"},
        "heading_hierarchy": {
            "type": "array",
            "items": {"type": "string"}
        },
        "chunk_type": {
            "type": "string",
            "enum": ["text", "table", "list", "register_diagram"]
        },
        "content": {"type": "string"}
    },
    "required": [
        "chunk_id", "source_file", "chapter_title", 
        "heading_hierarchy", "chunk_type", "content"
    ]
}

def isolate_tables(content: str) -> Tuple[str, List[str]]:
    """
    Phase 1: Identify and isolate tables in the content
    Returns content with tables replaced by placeholders and list of tables
    """
    tables = []
    protected_content = content
    for table_match in re.finditer(TABLE_PATTERN, content):
        placeholder = f"{{TABLE_{len(tables)}}}"
        protected_content = protected_content.replace(
            table_match.group(0), placeholder, 1
        )
        tables.append(table_match.group(0))
    return protected_content, tables

def build_chunks(
    protected_content: str, 
    source_file: str, 
    chapter_title: str, 
    tables: List[str]
) -> List[Dict]:
    """
    Phase 2: Build hierarchical chunks from the protected content
    """
    chunks = []
    current_hierarchy = []
    current_content = []
    current_level = 0
    
    for line in protected_content.split('\n'):
        heading_match = re.match(HEADING_PATTERN, line)
        if heading_match:
            # Save current chunk if exists
            if current_content:
                chunk = create_chunk(
                    current_hierarchy, 
                    current_content, 
                    source_file, 
                    chapter_title, 
                    tables
                )
                chunks.append(chunk)
                current_content = []
            
            # Update heading hierarchy
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            
            if level > current_level:
                current_hierarchy.append(heading_text)
            else:
                # Truncate hierarchy to current level and add new heading
                current_hierarchy = current_hierarchy[:level-1] + [heading_text]
            current_level = level
        else:
            current_content.append(line)
    
    # Add final chunk
    if current_content:
        chunk = create_chunk(
            current_hierarchy, 
            current_content, 
            source_file, 
            chapter_title, 
            tables
        )
        chunks.append(chunk)
    
    return chunks

def create_chunk(
    hierarchy: List[str], 
    content_lines: List[str], 
    source_file: str, 
    chapter_title: str, 
    tables: List[str]
) -> Dict:
    """Create a chunk dictionary from content lines and hierarchy"""
    content = '\n'.join(content_lines).strip()
    
    # Restore tables in content
    for i, table in enumerate(tables):
        placeholder = f"{{TABLE_{i}}}"
        content = content.replace(placeholder, table)
    
    # Generate chunk ID from hierarchy
    chunk_id = slugify('_'.join(hierarchy)) if hierarchy else "root"
    
    return {
        "chunk_id": chunk_id,
        "source_file": source_file,
        "chapter_title": chapter_title,
        "heading_hierarchy": hierarchy,
        "chunk_type": classify_chunk(content),
        "content": content
    }

def classify_chunk(content: str) -> str:
    """Classify chunk type based on content patterns"""
    if REGISTER_DIAGRAM_PATTERN.search(content):
        return "register_diagram"
    if re.search(TABLE_PATTERN, content):
        return "table"
    if LIST_PATTERN.search(content):
        return "list"
    return "text"

def validate_chunks(chunks: List[Dict], original_tables: List[str]) -> None:
    """
    Phase 3: Validate chunks against rules and schema
    """
    # Validate against JSON schema
    for chunk in chunks:
        validate(instance=chunk, schema=CHUNK_SCHEMA)
    
    # Check no table was split
    chunk_tables = [
        c["content"] for c in chunks 
        if c["chunk_type"] == "table"
    ]
    if len(chunk_tables) != len(original_tables):
        raise ValueError(
            f"Table count mismatch: {len(chunk_tables)} vs {len(original_tables)}"
        )
    
    # Check all tables are present
    for table in original_tables:
        if not any(table in chunk["content"] for chunk in chunks):
            raise ValueError(f"Table missing from chunks: {table[:50]}...")
    
    # Check hierarchy continuity
    hierarchy_levels = {}
    for chunk in chunks:
        for i, heading in enumerate(chunk["heading_hierarchy"]):
            if i not in hierarchy_levels:
                hierarchy_levels[i] = set()
            hierarchy_levels[i].add(heading)

def process_markdown_file(file_path: str) -> List[Dict]:
    """Process a markdown file and return JSON chunks"""
    # Extract chapter title from filename
    chapter_title = re.sub(r'\.md$', '', file_path.split('/')[-1])
    
    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Phase 1: Table isolation
    protected_content, tables = isolate_tables(content)
    
    # Phase 2: Hierarchical chunking
    chunks = build_chunks(
        protected_content, 
        file_path, 
        chapter_title, 
        tables
    )
    
    # Phase 3: Validation
    validate_chunks(chunks, tables)
    
    return chunks

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python chunk_processor.py <markdown_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    chunks = process_markdown_file(input_file)
    print(json.dumps(chunks, indent=2))