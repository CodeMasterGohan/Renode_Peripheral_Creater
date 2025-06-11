import unittest
import os
import json
from chunk_processor import process_markdown_file

class TestChunkProcessor(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_chapter.md"
        with open(self.test_file, 'w') as f:
            f.write("""### Test Chapter

## Section 1
This is a text paragraph.

- List item 1
- List item 2

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

## Section 2
Figure 3-4. Sample Register Diagram
<!-- image placeholder -->

### Subsection 2.1
More content here.
""")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_chunk_processing(self):
        chunks = process_markdown_file(self.test_file)
        
        # Should have 5 chunks: root, section1, list+table, section2, subsection2.1
        self.assertEqual(len(chunks), 5)
        
        # Verify chunk types
        chunk_types = [chunk["chunk_type"] for chunk in chunks]
        self.assertEqual(chunk_types, ["text", "text", "table", "register_diagram", "text"])
        
        # Verify hierarchy
        self.assertEqual(chunks[1]["heading_hierarchy"], ["Section 1"])
        self.assertEqual(chunks[4]["heading_hierarchy"], ["Section 2", "Subsection 2.1"])
        
        # Verify table preservation
        table_chunk = next(c for c in chunks if c["chunk_type"] == "table")
        self.assertIn("| Header 1 | Header 2 |", table_chunk["content"])
        
        # Verify register diagram detection
        reg_chunk = next(c for c in chunks if c["chunk_type"] == "register_diagram")
        self.assertIn("Figure 3-4. Sample Register Diagram", reg_chunk["content"])
        
        # Verify chunk IDs
        self.assertEqual(chunks[1]["chunk_id"], "section-1")
        self.assertEqual(chunks[4]["chunk_id"], "section-2_subsection-2-1")

if __name__ == "__main__":
    unittest.main()