# core/llm/factory.py
import os
from core.llm.deepseek_client import DeepSeekClient
from core.llm.openai_client import OpenAIClient

class LLMClientFactory:
    @staticmethod
    def create_client(provider: str):
        """
        Return an LLM client instance for the given provider.
        """
        if provider == "deepseek":
            # Suppose we store the key in an env variable DEEPSEEK_API_KEY
            api_key = os.getenv("DEEPSEEK_API_KEY", "fake-deepseek-key")
            return DeepSeekClient(api_key)
        elif provider == "openai":
            # Suppose we store the key in an env variable OPENAI_API_KEY
            api_key = os.getenv("OPENAI_API_KEY", "fake-openai-key")
            return OpenAIClient(api_key)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")