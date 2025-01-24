import openai
from typing import Optional
from core.llm_client import DeepSeekClient

class CodeGenerator:
    def __init__(self, api_key: str):
        self.client = DeepSeekClient(api_key)

    def generate_code(self, task: str, context: dict) -> str:
        system_msg = f"""You are a senior {context['language']} developer. 
        Write production-grade code following these constraints:
        - Use {context['framework']} framework
        - Follow {context['tech_stack']} conventions
        - Implement error handling"""
        
        return self.client.generate(
            prompt_type="coding",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": task}
            ]
        )