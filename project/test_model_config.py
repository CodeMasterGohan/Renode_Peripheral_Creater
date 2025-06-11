import unittest
from unittest.mock import patch, MagicMock
import yaml
import os
from model_manager import ModelManager, ModelConfig, ModelProvider
from milvus_rag_handler import MilvusRAGHandler, DocumentRetrievalError, MilvusConnectionError

class TestModelConfiguration(unittest.TestCase):
    """Test suite for model configuration implementation"""
    
    def setUp(self):
        # Create a valid config for testing
        self.valid_config = {
            'models': {
                'deepseek-r1-0528-free': {
                    'provider': 'openrouter',
                    'model_id': 'deepseek/deepseek-r1-0528:free',
                    'max_tokens': 8192,
                    'temperature_range': [0.1, 1.0],
                    'cost_per_1k_tokens': 0.0,
                    'supports_json': True,
                    'supports_functions': False,
                    'supports_system_prompt': True,
                    'rate_limit': 60,
                    'timeout': 120
                }
            }
        }
        
        # Create test config file
        with open('test_config.yaml', 'w') as f:
            yaml.dump(self.valid_config, f)
    
    def tearDown(self):
        # Clean up test file
        if os.path.exists('test_config.yaml'):
            os.remove('test_config.yaml')
    
    @patch('model_manager.ModelManager._init_providers')
    @patch('model_manager.ModelManager._init_models')
    def test_model_manager_config_loading(self, mock_init_models, mock_init_providers):
        """Test model manager loads configuration correctly"""
        # Mock the model initialization to use our test config
        mock_init_models.return_value = {
            'deepseek-r1-0528-free': ModelConfig(
                name='deepseek-r1-0528-free',
                provider=ModelProvider.OPENROUTER,
                model_id='deepseek/deepseek-r1-0528:free',
                max_tokens=8192,
                temperature_range=(0.1, 1.0),
                cost_per_1k_tokens=0.0,
                supports_json=True
            )
        }
        
        manager = ModelManager(config_path='test_config.yaml')
        
        # Verify models loaded
        self.assertIn('deepseek-r1-0528-free', manager.models)
        model = manager.models['deepseek-r1-0528-free']
        
        # Validate model properties
        self.assertEqual(model.provider, ModelProvider.OPENROUTER)
        self.assertEqual(model.model_id, 'deepseek/deepseek-r1-0528:free')
        self.assertEqual(model.max_tokens, 8192)
        self.assertEqual(model.temperature_range, (0.1, 1.0))
        self.assertEqual(model.cost_per_1k_tokens, 0.0)
        self.assertTrue(model.supports_json)
    
    def test_config_file_structure(self):
        """Test config file has required model section and parameters"""
        with open('test_config.yaml') as f:
            config = yaml.safe_load(f)
            
        # Verify models section exists
        self.assertIn('models', config)
        models = config['models']
        
        # Verify at least one model defined
        self.assertTrue(len(models) > 0)
        
        # Verify required parameters in first model
        model_name = list(models.keys())[0]
        model_config = models[model_name]
        
        required_params = [
            'provider', 'model_id', 'max_tokens',
            'temperature_range', 'cost_per_1k_tokens'
        ]
        
        for param in required_params:
            self.assertIn(param, model_config)
    
    @patch('milvus_rag_handler.MilvusRAGHandler._connect')
    @patch('milvus_rag_handler.MilvusRAGHandler._init_collection')
    def test_milvus_handler_config_usage(self, mock_init_collection, mock_connect):
        """Test Milvus handler uses config-defined embedding model"""
        # Create valid config with milvus section
        config = {
            'milvus': {
                'embedding_model': 'test-embedding',
                'host': 'localhost',
                'port': 19530,
                'embedding_dim': 768
            }
        }
        
        # Mock config loading
        with patch('milvus_rag_handler.yaml.safe_load', return_value=config):
            handler = MilvusRAGHandler(config_path='test_config.yaml')
            self.assertEqual(handler.embedding_model_name, 'test-embedding')
    
    def test_missing_model_config_error(self):
        """Test error when model config section is missing"""
        # Create invalid config without models section
        invalid_config = {
            'other_section': {},
            'milvus': {
                'embedding_model': 'test-embedding',
                'host': 'localhost',
                'port': 19530,
                'embedding_dim': 768
            }
        }
        with open('test_config.yaml', 'w') as f:
            yaml.dump(invalid_config, f)
        
        with self.assertRaises(KeyError) as context:
            ModelManager(config_path='test_config.yaml')
        
        self.assertIn("'models'", str(context.exception))
    
    @patch('model_manager.ModelManager._init_providers')
    @patch('model_manager.ModelManager._init_models')
    def test_invalid_model_name_error(self, mock_init_models, mock_init_providers):
        """Test error handling for invalid model names"""
        # Mock model initialization
        mock_init_models.return_value = {
            'model1': MagicMock()
        }
        
        manager = ModelManager(config_path='test_config.yaml')
        # Ensure model_preferences doesn't have the requested step
        manager.model_preferences = {'step1': 'model1'}
        
        with self.assertRaises(ValueError) as context:
            manager._get_model_for_step('invalid_step_name')
        
        self.assertIn("No model configured for step: invalid_step_name", str(context.exception))
    
    @patch('milvus_rag_handler.connections.connect')
    def test_unavailable_model_error(self, mock_connect):
        """Test error handling for unavailable models"""
        mock_connect.side_effect = Exception("Connection failed")
        
        with self.assertRaises(MilvusConnectionError) as context:
            MilvusRAGHandler(config_path='test_config.yaml')
        
        self.assertIn("Failed to connect to Milvus", str(context.exception))

if __name__ == '__main__':
    unittest.main()