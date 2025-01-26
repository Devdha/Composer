# core/llm/deepseek_client.py

from openai import OpenAI
from core.llm.prompt import Prompt
import logging

class DeepSeekClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.logger = logging.getLogger(__name__)

    def generate_code(self, prompt: Prompt) -> str:
        """
        Call to DeepSeek LLM API to generate code based on the prompt.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-reasoner",
                messages=prompt.get_messages()
            )
            content = response.choices[0].message.content
            return content
        except Exception as e:
            self.logger.error(f"Error generating code: {str(e)}", exc_info=True)
            raise