# core/llm/base_client.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import requests
import json
from config import settings


class BaseLLMClient(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        **kwargs
    ) -> str:
        """Base interface for all LLM providers"""
        pass

    @abstractmethod
    def get_usage_metrics(self) -> Dict[str, Any]:
        """Get token usage and costs"""
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: Dict) -> 'BaseLLMClient':
        """Factory method for configuration-based initialization"""
        pass

# core/llm/providers/deepseek.py
class DeepSeekClient(BaseLLMClient):
    def __init__(self, api_key: str, model: str = "deepseek-coder-33b-instruct"):
        self.api_key = api_key
        self.model = model
        self._session = self._create_session()
        
    def generate(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        response = self._session.post(
            "/chat/completions",
            json={
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7)
            }
        )
        return response.json()["choices"][0]["message"]["content"]

    @classmethod
    def from_config(cls, config: Dict) -> 'DeepSeekClient':
        return cls(
            api_key=config["DEEPSEEK_API_KEY"],
            model=config.get("MODEL", "deepseek-coder-33b-instruct")
        )

# core/llm/providers/openai.py
class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        # Similar implementation for OpenAI
        pass

# core/llm/factory.py
from importlib import import_module
from config import settings

class LLMClientFactory:
    _providers = {
        'deepseek': 'core.llm.providers.deepseek.DeepSeekClient',
        'openai': 'core.llm.providers.openai.OpenAIClient'
    }

    @classmethod
    def create_client(cls, provider: str = None) -> BaseLLMClient:
        provider = provider or settings.LLM_PROVIDER
        class_path = cls._providers[provider]
        
        module_path, class_name = class_path.rsplit('.', 1)
        module = import_module(module_path)
        client_class = getattr(module, class_name)
        
        return client_class.from_config(settings.LLM_CONFIG[provider])

    @classmethod
    def register_provider(cls, name: str, class_path: str):
        """Dynamically register new providers"""
        cls._providers[name] = class_path

class DeepSeekClient(BaseLLMClient):
    def __init__(self, config: dict):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        })
    
    def generate(self, **kwargs) -> str:
        response = self.session.post(
            f"{self.config['base_url']}/chat/completions",
            json={
                "model": self.config.get("model", "deepseek-coder-33b-instruct"),
                "messages": self._build_messages(kwargs),
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2048)
            }
        )
        return self._parse_response(response, kwargs.get("format"))
    
    def _build_messages(self, params: dict) -> list:
        messages = []
        if "system_message" in params:
            messages.append({"role": "system", "content": params["system_message"]})
        messages.append({"role": "user", "content": params["prompt"]})
        return messages
    
    def _parse_response(self, response: requests.Response, fmt: str) -> dict:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        if fmt == "yaml":
            return self._parse_yaml(content)
        elif fmt == "json":
            return json.loads(content)
        return content

    def get_usage_metrics(self) -> dict:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens
        }