import os
# Disable SSL verification for tests
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
from milvus_rag_handler import MilvusRAGHandler
import logging
import unittest
import tempfile
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO)

class TestMilvusRAGHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use test config file
        cls.handler = MilvusRAGHandler(config_path="project/test_config.yaml")
        # Create a temporary directory for test knowledge base
        cls.test_knowledge_dir = tempfile.mkdtemp()
        
        # Create test files: one .md and one .cs
        cls.md_file = os.path.join(cls.test_knowledge_dir, "test_doc.md")
        with open(cls.md_file, 'w') as f:
            f.write("""
            # Test Document
            This is a test document for the peripheral.
            ## Functional Description
            This section describes the functionality.
            """)
            
        cls.cs_file = os.path.join(cls.test_knowledge_dir, "test_example.cs")
        with open(cls.cs_file, 'w') as f:
            f.write("""
            // Test code example
            using System;
            class Example {
                void Run() {
                    Console.WriteLine("Hello World");
                }
            }
            """)
    
    @classmethod
    def tearDownClass(cls):
        # Clean up temporary directory
        shutil.rmtree(cls.test_knowledge_dir)
        # Close the handler
        cls.handler.close()
    
    def test_update_knowledge_base(self):
        # Get initial counts
        initial_stats = self.handler.get_collection_stats()
        initial_doc_count = initial_stats['document_collection']['num_entities']
        initial_example_count = initial_stats['example_collection']['num_entities']
        
        # Update knowledge base
        stats = self.handler.update_knowledge_base(self.test_knowledge_dir)
        
        # Check processing stats
        self.assertEqual(stats['processed'], 2)
        self.assertEqual(stats['errors'], 0)
        self.assertEqual(stats['docs'], 1)  # one .md file
        self.assertEqual(stats['code_examples'], 1)  # one .cs file
        
        # Check document collection count increased by the number of chunks from the .md file
        new_stats = self.handler.get_collection_stats()
        new_doc_count = new_stats['document_collection']['num_entities']
        new_example_count = new_stats['example_collection']['num_entities']
        
        # The .md file should have been chunked into multiple documents
        self.assertGreater(new_doc_count, initial_doc_count)
        # The .cs file should have been inserted as a single document
        self.assertEqual(new_example_count, initial_example_count + 1)
        
        # Verify metadata for code example
        example_results = self.handler.search_documents(
            query="code example",
            collection_name="renode_examples"
        )
        self.assertEqual(len(example_results), 1)
        self.assertEqual(example_results[0]['metadata']['type'], "code_example")
        self.assertEqual(example_results[0]['metadata']['title'], "test_example")

if __name__ == '__main__':
    unittest.main()