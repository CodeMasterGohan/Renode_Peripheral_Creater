"""
LLM Model Manager with Multi-Provider Support and Accuracy Framework

This module provides a unified interface for managing multiple LLM providers
with built-in accuracy tracking, response validation, retry mechanisms,
and advanced features like A/B testing and confidence scoring.

Key features:
- Multi-provider support (OpenAI, Anthropic, Gemini, Groq, Ollama)
- Response validation against JSON schemas
- Automatic retry with prompt optimization
- Confidence scoring and accuracy tracking
- A/B testing for model comparison
- Response caching and rate limiting
- Comprehensive logging and metrics

Author: Renode Model Generator Team
Version: 2.0.0
"""

import asyncio
import hashlib
import json
import logging
import os
import re
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Callable, Tuple
from threading import Lock
import yaml

# Third-party imports
import openai
import anthropic
import google.generativeai as genai
from groq import Groq
import httpx
import tiktoken
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from jsonschema import validate, ValidationError as JsonValidationError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ModelProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    GROQ = "groq"
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"


@dataclass
class ModelConfig:
    """Configuration for an LLM model."""
    name: str
    provider: ModelProvider
    model_id: str
    max_tokens: int
    temperature_range: Tuple[float, float]
    cost_per_1k_tokens: float
    supports_json: bool = False
    supports_functions: bool = False
    supports_system_prompt: bool = True
    rate_limit: int = 60  # requests per minute
    timeout: int = 120  # seconds
    
    # Performance tracking
    total_calls: int = field(default=0, init=False)
    total_tokens: int = field(default=0, init=False)
    total_cost: float = field(default=0.0, init=False)
    accuracy_scores: List[float] = field(default_factory=list, init=False)
    response_times: List[float] = field(default_factory=list, init=False)
    validation_failures: int = field(default=0, init=False)
    retry_counts: List[int] = field(default_factory=list, init=False)


@dataclass
class GenerationResult:
    """Result of an LLM generation."""
    content: str
    model: str
    provider: ModelProvider
    prompt_tokens: int
    response_tokens: int
    total_tokens: int
    response_time: float
    cost: float
    confidence_score: float
    validation_passed: bool
    retry_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, max_calls: int, time_window: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum calls allowed
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
        self.lock = Lock()
    
    def acquire(self) -> bool:
        """Check if a call can be made."""
        with self.lock:
            now = time.time()
            # Remove old calls outside the time window
            self.calls = [t for t in self.calls if now - t < self.time_window]
            
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True
            return False
    
    def wait_time(self) -> float:
        """Get time to wait before next call."""
        with self.lock:
            if not self.calls:
                return 0
            
            oldest_call = min(self.calls)
            wait = self.time_window - (time.time() - oldest_call)
            return max(0, wait)


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize provider with optional API key."""
        self.api_key = api_key
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response from LLM."""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str, model: str) -> int:
        """Count tokens in text."""
        pass
    
    def validate_response(self, response: str, response_format: Optional[str]) -> bool:
        """Basic response validation."""
        if response_format == "json":
            try:
                json.loads(response)
                return True
            except json.JSONDecodeError:
                return False
        return bool(response.strip())


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI provider."""
        super().__init__(api_key or os.getenv("OPENAI_API_KEY"))
        self.client = openai.OpenAI(api_key=self.api_key)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((openai.RateLimitError, openai.APITimeoutError))
    )
    def generate(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response using OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if response_format == "json":
            params["response_format"] = {"type": "json_object"}
        
        # Add any additional parameters
        params.update(kwargs)
        
        response = self.client.chat.completions.create(**params)
        return response.choices[0].message.content
    
    def count_tokens(self, text: str, model: str) -> int:
        """Count tokens using tiktoken."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        return len(encoding.encode(text))


class OpenRouterError(Exception):
    """Base exception for OpenRouter errors."""
    pass

class OpenRouterConfigError(OpenRouterError):
    """Exception for configuration errors."""
    pass

class OpenRouterRateLimitError(OpenRouterError):
    """Exception for rate limiting errors."""
    pass

class OpenRouterAPIError(OpenRouterError):
    """Exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter API provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenRouter provider with configuration validation."""
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise OpenRouterConfigError("OPENROUTER_API_KEY is required but not provided")
        
        if not isinstance(api_key, str) or not api_key.startswith("sk-"):
            raise OpenRouterConfigError("Invalid OPENROUTER_API_KEY format")
            
        super().__init__(api_key)
        self.base_url = "https://api.openrouter.ai/v1"
        self.client = httpx.Client(timeout=120.0)
        self.rate_limiter = RateLimiter(60)  # OpenRouter's default rate limit
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((OpenRouterRateLimitError, httpx.TimeoutException))
    )
    def generate(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response using OpenRouter API with enhanced error handling."""
        if not self.rate_limiter.acquire():
            wait_time = self.rate_limiter.wait_time()
            self.logger.warning(f"Rate limited - waiting {wait_time:.1f}s before retry")
            raise OpenRouterRateLimitError(f"Rate limit exceeded. Try again in {wait_time:.1f} seconds")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/dso-mil/Renode_Peripheral_Creater",
            "X-Title": "Renode Peripheral Creator"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if response_format == "json":
            payload["response_format"] = {"type": "json_object"}
        
        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120.0
            )
            
            # Handle different HTTP status codes
            if response.status_code == 429:
                retry_after = int(response.headers.get('retry-after', 60))
                raise OpenRouterRateLimitError(f"Rate limited. Retry after {retry_after} seconds")
            
            response.raise_for_status()
            
            try:
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"]
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error(f"Failed to parse OpenRouter response: {e}")
                raise OpenRouterAPIError("Invalid response format from OpenRouter")
                
        except httpx.HTTPStatusError as e:
            error_msg = f"OpenRouter API request failed with status {e.response.status_code}"
            self.logger.error(f"{error_msg}: {e}")
            raise OpenRouterAPIError(error_msg, e.response.status_code)
        except httpx.TimeoutException as e:
            self.logger.warning(f"OpenRouter API timeout: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected OpenRouter API error: {e}")
            raise OpenRouterAPIError(f"Unexpected error: {str(e)}")
    
    def count_tokens(self, text: str, model: str) -> int:
        """Estimate token count using tiktoken."""
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except:
            return len(text) // 4


class AnthropicProvider(BaseLLMProvider):
    """Anthropic API provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Anthropic provider."""
        super().__init__(api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APITimeoutError))
    )
    def generate(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response using Anthropic API."""
        messages = [{"role": "user", "content": prompt}]
        
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if system_prompt:
            params["system"] = system_prompt
        
        response = self.client.messages.create(**params)
        content = response.content[0].text
        
        # Handle JSON format request
        if response_format == "json":
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    json.loads(json_match.group())
                    content = json_match.group()
                except json.JSONDecodeError:
                    pass
        
        return content
    
    def count_tokens(self, text: str, model: str) -> int:
        """Estimate token count for Anthropic models."""
        # Rough estimation: 1 token ≈ 4 characters
        return len(text) // 4


class GeminiProvider(BaseLLMProvider):
    """Google Gemini API provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini provider."""
        super().__init__(api_key or os.getenv("GEMINI_API_KEY"))
        genai.configure(api_key=self.api_key)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response using Gemini API."""
        model_instance = genai.GenerativeModel(model)
        
        # Combine system prompt with user prompt if provided
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        # Configure generation settings
        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        response = model_instance.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        
        content = response.text
        
        # Handle JSON format request
        if response_format == "json":
            # Add instruction to return JSON
            json_prompt = f"{full_prompt}\n\nReturn your response as valid JSON."
            response = model_instance.generate_content(
                json_prompt,
                generation_config=generation_config
            )
            content = response.text
        
        return content
    
    def count_tokens(self, text: str, model: str) -> int:
        """Count tokens for Gemini models."""
        model_instance = genai.GenerativeModel(model)
        return model_instance.count_tokens(text).total_tokens


class GroqProvider(BaseLLMProvider):
    """Groq API provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq provider."""
        super().__init__(api_key or os.getenv("GROQ_API_KEY"))
        self.client = Groq(api_key=self.api_key)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response using Groq API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        content = response.choices[0].message.content
        
        # Handle JSON format request
        if response_format == "json":
            # Try to ensure valid JSON
            try:
                json.loads(content)
            except json.JSONDecodeError:
                # Retry with explicit JSON instruction
                messages[-1]["content"] += "\n\nPlease return your response as valid JSON."
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                content = response.choices[0].message.content
        
        return content
    
    def count_tokens(self, text: str, model: str) -> int:
        """Estimate token count for Groq models."""
        # Use tiktoken for estimation
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except:
            # Fallback to character-based estimation
            return len(text) // 4


class OllamaProvider(BaseLLMProvider):
    """Ollama local model provider implementation."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize Ollama provider."""
        super().__init__()
        self.base_url = base_url
        self.client = httpx.Client(timeout=120.0)
    
    def generate(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response using Ollama API."""
        # Combine system prompt with user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        # Add JSON instruction if needed
        if response_format == "json":
            full_prompt += "\n\nReturn your response as valid JSON."
        
        payload = {
            "model": model,
            "prompt": full_prompt,
            "temperature": temperature,
            "options": {
                "num_predict": max_tokens
            }
        }
        
        try:
            response = self.client.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120.0
            )
            response.raise_for_status()
            
            # Ollama returns streaming responses - we need to parse each JSON line
            full_response = ""
            for line in response.text.strip().split('\n'):
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            full_response += data["response"]
                        elif "error" in data:
                            self.logger.error(f"Ollama error: {data['error']}")
                            raise Exception(f"Ollama error: {data['error']}")
                    except json.JSONDecodeError as e:
                        self.logger.error(f"Failed to parse Ollama response: {e}")
                        raise
            
            return full_response
            
        except Exception as e:
            self.logger.error(f"Ollama generation error: {e}")
            raise
    
    def count_tokens(self, text: str, model: str) -> int:
        """Estimate token count for Ollama models."""
        # Simple estimation
        return len(text.split())


class ModelManager:
    """Manages multiple LLM models with accuracy tracking and advanced features."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize model manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize rate limiters early
        self.rate_limiters = {}
        
        # Initialize providers
        self.providers = self._init_providers()
        
        # Initialize models
        self.models = self._init_models()
        
        # Response cache
        self.cache = {}
        self.cache_lock = Lock()
        self.cache_hits = 0
        self.cache_ttl = self.config.get("cache", {}).get("response_cache", {}).get("ttl", 3600)
        
        # Metrics
        self.total_calls = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.validation_failures = 0
        
        # Thread pool for parallel execution
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Try default config path
        default_path = Path("config.yaml")
        if default_path.exists():
            with open(default_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Return minimal default config
        return {
            "models": {},
            "validation": {"strict_mode": True},
            "cache": {"response_cache": {"enabled": True, "ttl": 3600}}
        }
    
    def _init_providers(self) -> Dict[ModelProvider, BaseLLMProvider]:
        """Initialize LLM providers."""
        providers = {}
        
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            providers[ModelProvider.OPENAI] = OpenAIProvider()
            self.logger.info("Initialized OpenAI provider")
        
        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            providers[ModelProvider.ANTHROPIC] = AnthropicProvider()
            self.logger.info("Initialized Anthropic provider")
        
        # Gemini
        if os.getenv("GEMINI_API_KEY"):
            providers[ModelProvider.GEMINI] = GeminiProvider()
            self.logger.info("Initialized Gemini provider")
        
        # Groq
        if os.getenv("GROQ_API_KEY"):
            providers[ModelProvider.GROQ] = GroqProvider()
            self.logger.info("Initialized Groq provider")
        
        # OpenRouter
        if os.getenv("OPENROUTER_API_KEY"):
            providers[ModelProvider.OPENROUTER] = OpenRouterProvider()
            self.logger.info("Initialized OpenRouter provider")

        # Ollama (check if running)
        try:
            ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            response = httpx.get(f"{ollama_url}/api/tags", timeout=5.0)
            if response.status_code == 200:
                providers[ModelProvider.OLLAMA] = OllamaProvider(ollama_url)
                self.logger.info("Initialized Ollama provider")
        except:
            pass
        
        return providers
    
    def _init_models(self) -> Dict[str, ModelConfig]:
        """Initialize model configurations."""
        models = {}
        
        # OpenAI models
        if ModelProvider.OPENAI in self.providers:
            models["gpt-4"] = ModelConfig(
                name="gpt-4",
                provider=ModelProvider.OPENAI,
                model_id="gpt-4",
                max_tokens=8192,
                temperature_range=(0.0, 2.0),
                cost_per_1k_tokens=0.03,
                supports_json=True,
                supports_functions=True,
                rate_limit=10000
            )
            
            models["gpt-4-turbo"] = ModelConfig(
                name="gpt-4-turbo",
                provider=ModelProvider.OPENAI,
                model_id="gpt-4-turbo-preview",
                max_tokens=128000,
                temperature_range=(0.0, 2.0),
                cost_per_1k_tokens=0.01,
                supports_json=True,
                supports_functions=True,
                rate_limit=10000
            )
            
            models["gpt-3.5-turbo"] = ModelConfig(
                name="gpt-3.5-turbo",
                provider=ModelProvider.OPENAI,
                model_id="gpt-3.5-turbo",
                max_tokens=16384,
                temperature_range=(0.0, 2.0),
                cost_per_1k_tokens=0.001,
                supports_json=True,
                supports_functions=True,
                rate_limit=10000
            )
        
        # Anthropic models
        if ModelProvider.ANTHROPIC in self.providers:
            models["claude-3-opus"] = ModelConfig(
                name="claude-3-opus",
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-opus-20240229",
                max_tokens=200000,
                temperature_range=(0.0, 1.0),
                cost_per_1k_tokens=0.015,
                supports_json=False,
                supports_functions=False,
                rate_limit=1000
            )
            
            models["claude-3-sonnet"] = ModelConfig(
                name="claude-3-sonnet",
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-sonnet-20240229",
                max_tokens=200000,
                temperature_range=(0.0, 1.0),
                cost_per_1k_tokens=0.003,
                supports_json=False,
                supports_functions=False,
                rate_limit=1000
            )
            
            models["claude-3-haiku"] = ModelConfig(
                name="claude-3-haiku",
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-haiku-20240307",
                max_tokens=200000,
                temperature_range=(0.0, 1.0),
                cost_per_1k_tokens=0.00025,
                supports_json=False,
                supports_functions=False,
                rate_limit=1000
            )
        
        # OpenRouter models
        if ModelProvider.OPENROUTER in self.providers:
            models["openrouter/anthropic/claude-3-opus"] = ModelConfig(
                name="openrouter/anthropic/claude-3-opus",
                provider=ModelProvider.OPENROUTER,
                model_id="anthropic/claude-3-opus",
                max_tokens=200000,
                temperature_range=(0.0, 1.0),
                cost_per_1k_tokens=0.015,
                supports_json=False,
                supports_functions=False,
                rate_limit=1000
            )
            
            models["openrouter/openai/gpt-4-turbo"] = ModelConfig(
                name="openrouter/openai/gpt-4-turbo",
                provider=ModelProvider.OPENROUTER,
                model_id="openai/gpt-4-turbo-preview",
                max_tokens=128000,
                temperature_range=(0.0, 2.0),
                cost_per_1k_tokens=0.01,
                supports_json=True,
                supports_functions=True,
                rate_limit=10000
            )
            
            models["openrouter/meta-llama/llama-3-70b"] = ModelConfig(
                name="openrouter/meta-llama/llama-3-70b",
                provider=ModelProvider.OPENROUTER,
                model_id="meta-llama/llama-3-70b-instruct",
                max_tokens=8192,
                temperature_range=(0.0, 2.0),
                cost_per_1k_tokens=0.0005,
                supports_json=False,
                supports_functions=False,
                rate_limit=1000
            )

        # Gemini models
        if ModelProvider.GEMINI in self.providers:
            models["gemini-pro"] = ModelConfig(
                name="gemini-pro",
                provider=ModelProvider.GEMINI,
                model_id="gemini-pro",
                max_tokens=30720,
                temperature_range=(0.0, 1.0),
                cost_per_1k_tokens=0.00025,
                supports_json=False,
                supports_functions=False,
                rate_limit=60
            )
            
            models["gemini-pro-vision"] = ModelConfig(
                name="gemini-pro-vision",
                provider=ModelProvider.GEMINI,
                model_id="gemini-pro-vision",
                max_tokens=12288,
                temperature_range=(0.0, 1.0),
                cost_per_1k_tokens=0.00025,
                supports_json=False,
                supports_functions=False,
                rate_limit=60
            )
        
        # Groq models
        if ModelProvider.GROQ in self.providers:
            models["mixtral-8x7b"] = ModelConfig(
                name="mixtral-8x7b",
                provider=ModelProvider.GROQ,
                model_id="mixtral-8x7b-32768",
                max_tokens=32768,
                temperature_range=(0.0, 1.0),
                cost_per_1k_tokens=0.00027,
                supports_json=False,
                supports_functions=False,
                rate_limit=30
            )
            
            models["llama2-70b"] = ModelConfig(
                name="llama2-70b",
                provider=ModelProvider.GROQ,
                model_id="llama2-70b-4096",
                max_tokens=4096,
                temperature_range=(0.0, 1.0),
                cost_per_1k_tokens=0.00064,
                supports_json=False,
                supports_functions=False,
                rate_limit=30
            )
        
        # Ollama models (if available)
        if ModelProvider.OLLAMA in self.providers:
            # Check available models
            try:
                ollama = self.providers[ModelProvider.OLLAMA]
                response = ollama.client.get(f"{ollama.base_url}/api/tags")
                if response.status_code == 200:
                    available_models = response.json().get("models", [])
                    for model_info in available_models:
                        model_name = model_info["name"]
                        models[f"ollama/{model_name}"] = ModelConfig(
                            name=f"ollama/{model_name}",
                            provider=ModelProvider.OLLAMA,
                            model_id=model_name,
                            max_tokens=4096,
                            temperature_range=(0.0, 1.0),
                            cost_per_1k_tokens=0.0,  # Local models are free
                            supports_json=False,
                            supports_functions=False,
                            rate_limit=1000  # No real limit for local
                        )
            except:
                pass
        
        # Initialize rate limiters
        for model_name, model_config in models.items():
            self.rate_limiters[model_name] = RateLimiter(model_config.rate_limit)
        
        return models
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        validation_schema: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        cache_key: Optional[str] = None,
        step_name: Optional[str] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate response with validation and retry logic.
        
        Args:
            prompt: Input prompt
            model: Model name (uses config preference if not specified)
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            system_prompt: System prompt for the model
            response_format: Response format (e.g., "json")
            validation_schema: JSON schema for validation
            max_retries: Maximum retry attempts
            cache_key: Cache key for response caching
            step_name: Pipeline step name for model selection
            **kwargs: Additional model-specific parameters
            
        Returns:
            GenerationResult with response and metadata
        """
        # Select model based on step or use provided
        if not model and step_name:
            model = self._get_model_for_step(step_name)
        elif not model:
            model = self._get_default_model()
        
        # Check cache
        if cache_key and self._check_cache(cache_key):
            return self._get_cached_result(cache_key)
        
        # Validate model exists
        if model not in self.models:
            raise ValueError(f"Unknown model: {model}")
        
        model_config = self.models[model]
        
        # Set defaults
        if max_tokens is None:
            max_tokens = min(4096, model_config.max_tokens)
        
        # Clamp temperature
        temperature = max(model_config.temperature_range[0],
                         min(temperature, model_config.temperature_range[1]))
        
        # Rate limiting
        rate_limiter = self.rate_limiters[model]
        while not rate_limiter.acquire():
            wait_time = rate_limiter.wait_time()
            self.logger.info(f"Rate limit reached for {model}, waiting {wait_time:.1f}s")
            time.sleep(wait_time)
        
        # Retry loop with prompt optimization
        retry_count = 0
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Modify prompt for retries
                current_prompt = prompt
                current_temp = temperature
                
                if attempt > 0:
                    current_prompt = self._optimize_prompt_for_retry(
                        prompt, response_format, validation_schema, attempt
                    )
                    # Increase temperature slightly for variety
                    current_temp = min(temperature + (0.1 * attempt), 
                                     model_config.temperature_range[1])
                
                # Generate response
                result = self._generate_single(
                    model=model,
                    prompt=current_prompt,
                    temperature=current_temp,
                    max_tokens=max_tokens,
                    system_prompt=system_prompt,
                    response_format=response_format,
                    **kwargs
                )
                
                # Validate response
                validation_passed = True
                if validation_schema:
                    validation_passed = self._validate_response(
                        result.content, validation_schema, response_format
                    )
                    if not validation_passed:
                        model_config.validation_failures += 1
                        self.validation_failures += 1
                        if attempt < max_retries - 1:
                            self.logger.warning(
                                f"Validation failed for {model}, attempt {attempt + 1}/{max_retries}"
                            )
                            continue
                
                # Calculate confidence score
                confidence_score = self._calculate_confidence_score(
                    result, validation_passed, retry_count
                )
                
                # Update result
                result.validation_passed = validation_passed
                result.confidence_score = confidence_score
                result.retry_count = retry_count
                
                # Cache successful result
                if cache_key and validation_passed:
                    self._cache_result(cache_key, result)
                
                # Update metrics
                model_config.retry_counts.append(retry_count)
                
                return result
                
            except Exception as e:
                last_error = e
                retry_count += 1
                self.logger.error(f"Generation error on attempt {attempt + 1}: {e}")
                
                if attempt < max_retries - 1:
                    # Try fallback model
                    fallback = self._get_fallback_model(model)
                    if fallback and fallback != model:
                        self.logger.info(f"Trying fallback model: {fallback}")
                        model = fallback
                        model_config = self.models[model]
        
        # All retries failed
        raise RuntimeError(f"Generation failed after {max_retries} attempts: {last_error}")
    
    def generate_parallel(
        self,
        prompt: str,
        models: List[str],
        **kwargs
    ) -> List[GenerationResult]:
        """
        Generate responses from multiple models in parallel (A/B testing).
        
        Args:
            prompt: Input prompt
            models: List of model names to use
            **kwargs: Additional generation parameters
            
        Returns:
            List of GenerationResult objects
        """
        futures = []
        results = []
        
        # Submit generation tasks
        for model in models:
            future = self.executor.submit(
                self.generate,
                prompt=prompt,
                model=model,
                **kwargs
            )
            futures.append((model, future))
        
        # Collect results
        for model, future in futures:
            try:
                result = future.result(timeout=120)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Parallel generation failed for {model}: {e}")
                # Create a failed result
                results.append(GenerationResult(
                    content="",
                    model=model,
                    provider=self.models[model].provider if model in self.models else ModelProvider.OPENAI,
                    prompt_tokens=0,
                    response_tokens=0,
                    total_tokens=0,
                    response_time=0.0,
                    cost=0.0,
                    confidence_score=0.0,
                    validation_passed=False,
                    retry_count=0,
                    metadata={"error": str(e)}
                ))
        
        return results
    
    def _generate_single(
        self,
        model: str,
        prompt: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> GenerationResult:
        """Generate a single response without retry logic."""
        model_config = self.models[model]
        provider = self.providers[model_config.provider]
        
        # Track timing
        start_time = time.time()
        
        # Generate response
        content = provider.generate(
            prompt=prompt,
            model=model_config.model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            response_format=response_format,
            **kwargs
        )
        
        # Calculate metrics
        response_time = time.time() - start_time
        prompt_tokens = provider.count_tokens(prompt, model_config.model_id)
        if system_prompt:
            prompt_tokens += provider.count_tokens(system_prompt, model_config.model_id)
        response_tokens = provider.count_tokens(content, model_config.model_id)
        total_tokens = prompt_tokens + response_tokens
        cost = (total_tokens / 1000) * model_config.cost_per_1k_tokens
        
        # Update model metrics
        model_config.total_calls += 1
        model_config.total_tokens += total_tokens
        model_config.total_cost += cost
        model_config.response_times.append(response_time)
        
        # Update global metrics
        self.total_calls += 1
        self.total_tokens += total_tokens
        self.total_cost += cost
        
        # Log generation
        self._log_generation(
            model=model,
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens,
            response_time=response_time,
            cost=cost
        )
        
        return GenerationResult(
            content=content,
            model=model,
            provider=model_config.provider,
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens,
            total_tokens=total_tokens,
            response_time=response_time,
            cost=cost,
            confidence_score=0.0,  # Will be calculated later
            validation_passed=True,  # Will be validated later
            retry_count=0
        )
    
    def _optimize_prompt_for_retry(
        self,
        original_prompt: str,
        response_format: Optional[str],
        validation_schema: Optional[Dict[str, Any]],
        attempt: int
    ) -> str:
        """Optimize prompt for retry attempts."""
        optimized = original_prompt
        
        # Add format clarification
        if response_format == "json":
            optimized += "\n\nIMPORTANT: Return your response as valid JSON only, with no additional text."
        
        # Add schema hints
        if validation_schema and attempt > 0:
            required_fields = validation_schema.get("required", [])
            if required_fields:
                optimized += f"\n\nRequired fields: {', '.join(required_fields)}"
            
            # Add example structure
            if attempt > 1:
                properties = validation_schema.get("properties", {})
                example = {}
                for field, schema in properties.items():
                    if schema.get("type") == "string":
                        example[field] = "example_value"
                    elif schema.get("type") == "number":
                        example[field] = 0
                    elif schema.get("type") == "boolean":
                        example[field] = True
                    elif schema.get("type") == "array":
                        example[field] = []
                    elif schema.get("type") == "object":
                        example[field] = {}
                
                optimized += f"\n\nExample structure:\n{json.dumps(example, indent=2)}"
        
        return optimized
    
    def _validate_response(
        self,
        content: str,
        validation_schema: Dict[str, Any],
        response_format: Optional[str]
    ) -> bool:
        """Validate response against schema."""
        try:
            # Parse JSON if needed
            if response_format == "json":
                data = json.loads(content)
                # Validate against schema
                validate(instance=data, schema=validation_schema)
            else:
                # For non-JSON, just check if content exists
                if not content.strip():
                    return False
            
            return True
            
        except (json.JSONDecodeError, JsonValidationError) as e:
            self.logger.debug(f"Validation error: {e}")
            return False
    
    def _calculate_confidence_score(
        self,
        result: GenerationResult,
        validation_passed: bool,
        retry_count: int
    ) -> float:
        """Calculate confidence score for a generation."""
        score = 1.0
        
        # Validation penalty
        if not validation_passed:
            score *= 0.5
        
        # Retry penalty
        score *= (1.0 - (retry_count * 0.1))
        
        # Response time penalty (slower = less confident)
        if result.response_time > 10:
            score *= 0.9
        elif result.response_time > 20:
            score *= 0.8
        
        # Token usage penalty (very long = potentially rambling)
        if result.response_tokens > 2000:
            score *= 0.95
        
        # Model-specific adjustments
        model_config = self.models.get(result.model)
        if model_config:
            # Use historical accuracy if available
            if model_config.accuracy_scores:
                avg_accuracy = sum(model_config.accuracy_scores) / len(model_config.accuracy_scores)
                score *= avg_accuracy
        
        return max(0.0, min(1.0, score))
    
    def _get_model_for_step(self, step_name: str) -> str:
        """Get preferred model for a pipeline step."""
        preferences = self.config.get("models", {}).get("preferences", {})
        
        # Map step names to preference keys
        step_mapping = {
            "analysis": "analysis",
            "todo_generation": "analysis",
            "interface_definition": "code_generation",
            "implementation": "code_generation",
            "test_generation": "testing",
            "documentation": "documentation"
        }
        
        preference_key = step_mapping.get(step_name, "analysis")
        preferred_model = preferences.get(preference_key)
        
        # Check if model is available
        if preferred_model and preferred_model in self.models:
            return preferred_model
        
        # Fallback to default
        return self._get_default_model()
    
    def _get_default_model(self) -> str:
        """Get default model based on availability."""
        # Priority order
        priority = [
            "gpt-4",
            "claude-3-opus",
            "gpt-4-turbo",
            "claude-3-sonnet",
            "gemini-pro",
            "mixtral-8x7b",
            "gpt-3.5-turbo",
            "claude-3-haiku"
        ]
        
        for model in priority:
            if model in self.models:
                return model
        
        # Return first available model
        if self.models:
            return list(self.models.keys())[0]
        
        raise ValueError("No models available")
    
    def _get_fallback_model(self, failed_model: str) -> Optional[str]:
        """Get fallback model for failed generation."""
        fallback_map = {
            "gpt-4": "gpt-4-turbo",
            "gpt-4-turbo": "gpt-3.5-turbo",
            "gpt-3.5-turbo": "claude-3-sonnet",
            "claude-3-opus": "claude-3-sonnet",
            "claude-3-sonnet": "claude-3-haiku",
            "claude-3-haiku": "gpt-3.5-turbo",
            "gemini-pro": "gpt-3.5-turbo",
            "mixtral-8x7b": "llama2-70b",
            "llama2-70b": "gpt-3.5-turbo"
        }
        
        fallback = fallback_map.get(failed_model)
        if fallback and fallback in self.models:
            return fallback
        
        # Try to find any other available model
        for model in self.models:
            if model != failed_model:
                return model
        
        return None
    
    def _check_cache(self, cache_key: str) -> bool:
        """Check if result exists in cache."""
        with self.cache_lock:
            if cache_key in self.cache:
                # Check TTL
                cached_time, _ = self.cache[cache_key]
                if time.time() - cached_time < self.cache_ttl:
                    self.cache_hits += 1
                    return True
                else:
                    # Expired
                    del self.cache[cache_key]
        return False
    
    def _get_cached_result(self, cache_key: str) -> GenerationResult:
        """Get cached result."""
        with self.cache_lock:
            _, result = self.cache[cache_key]
            self.logger.info(f"Cache hit for key: {cache_key}")
            return result
    
    def _cache_result(self, cache_key: str, result: GenerationResult) -> None:
        """Cache a result."""
        with self.cache_lock:
            self.cache[cache_key] = (time.time(), result)
            
            # Limit cache size
            max_size = self.config.get("cache", {}).get("response_cache", {}).get("max_size", 1000)
            if len(self.cache) > max_size:
                # Remove oldest entries
                sorted_keys = sorted(self.cache.keys(), key=lambda k: self.cache[k][0])
                for key in sorted_keys[:len(self.cache) - max_size]:
                    del self.cache[key]
    
    def _log_generation(
        self,
        model: str,
        prompt_tokens: int,
        response_tokens: int,
        response_time: float,
        cost: float
    ) -> None:
        """Log generation details."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": prompt_tokens + response_tokens,
            "response_time": response_time,
            "cost": cost
        }
        
        # Write to log file
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_path = log_dir / "model_usage.jsonl"
        
        with open(str(log_path), 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics for all models."""
        metrics = {
            "total_calls": self.total_calls,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "cache_hits": self.cache_hits,
            "cache_size": len(self.cache),
            "validation_failures": self.validation_failures,
            "models": {}
        }
        
        for name, model in self.models.items():
            metrics["models"][name] = {
                "calls": model.total_calls,
                "tokens": model.total_tokens,
                "cost": model.total_cost,
                "validation_failures": model.validation_failures,
                "avg_accuracy": sum(model.accuracy_scores) / len(model.accuracy_scores) if model.accuracy_scores else None,
                "avg_response_time": sum(model.response_times) / len(model.response_times) if model.response_times else None,
                "avg_retry_count": sum(model.retry_counts) / len(model.retry_counts) if model.retry_counts else None
            }
        
        return metrics
    
    def get_best_model_for_task(
        self,
        task_type: str,
        requirements: Optional[Dict[str, Any]] = None
    ) -> str:
        """Select best model based on task requirements and performance."""
        if requirements is None:
            requirements = {}
        
        candidates = []
        
        for name, model in self.models.items():
            # Check requirements
            if requirements.get("json_support") and not model.supports_json:
                continue
            
            if requirements.get("min_tokens", 0) > model.max_tokens:
                continue
            
            if requirements.get("max_cost_per_1k", float('inf')) < model.cost_per_1k_tokens:
                continue
            
            # Calculate score
            score = self._calculate_model_score(model, task_type)
            candidates.append((name, score))
        
        if not candidates:
            raise ValueError("No suitable model found for requirements")
        
        # Sort by score
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    def _calculate_model_score(self, model: ModelConfig, task_type: str) -> float:
        """Calculate model score based on performance and task type."""
        score = 50.0
        
        # Historical performance
        if model.accuracy_scores:
            avg_accuracy = sum(model.accuracy_scores) / len(model.accuracy_scores)
            score += avg_accuracy * 30
        
        # Response time
        if model.response_times:
            avg_time = sum(model.response_times) / len(model.response_times)
            time_score = max(0, 20 - (avg_time / 10))
            score += time_score
        
        # Cost efficiency
        cost_score = 10 / (1 + model.cost_per_1k_tokens)
        score += cost_score
        
        # Validation success rate
        if model.total_calls > 0:
            success_rate = 1 - (model.validation_failures / model.total_calls)
            score += success_rate * 10
        
        # Task-specific bonuses
        task_bonuses = {
            "code_generation": {
                "claude-3-opus": 15,
                "gpt-4": 12,
                "gpt-4-turbo": 10
            },
            "analysis": {
                "gpt-4": 15,
                "claude-3-opus": 12,
                "gemini-pro": 8
            },
            "testing": {
                "gpt-4": 15,
                "gpt-4-turbo": 12,
                "claude-3-sonnet": 8
            },
            "documentation": {
                "gpt-4-turbo": 15,
                "claude-3-opus": 12,
                "gpt-4": 10
            }
        }
        
        if task_type in task_bonuses and model.name in task_bonuses[task_type]:
            score += task_bonuses[task_type][model.name]
        
        return score
    
    def clear_cache(self) -> None:
        """Clear response cache."""
        with self.cache_lock:
            self.cache.clear()
            self.logger.info("Response cache cleared")
    def list_available_models(self) -> List[str]:
        """List the names of all available models."""
        return list(self.models.keys())
    
    def shutdown(self) -> None:
        """Shutdown model manager and cleanup resources."""
        self.executor.shutdown(wait=True)
        self.clear_cache()
        
        # Close any open connections
        for provider in self.providers.values():
            if hasattr(provider, 'client') and hasattr(provider.client, 'close'):
                provider.client.close()
        
        self.logger.info("Model manager shutdown complete")


# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize manager
    manager = ModelManager()
    
    # Generate response
    result = manager.generate(
        prompt="Write a simple Python function to calculate factorial",
        model="gpt-4",
        temperature=0.3,
        response_format="json",
        validation_schema={
            "type": "object",
            "properties": {
                "code": {"type": "string"},
                "explanation": {"type": "string"}
            },
            "required": ["code", "explanation"]
        }
    )
    
    print(f"Model: {result.model}")
    print(f"Response: {result.content}")
    print(f"Confidence: {result.confidence_score:.2f}")
    print(f"Cost: ${result.cost:.4f}")
    
    # Get metrics
    metrics = manager.get_metrics()
    print(f"\nMetrics: {json.dumps(metrics, indent=2)}")