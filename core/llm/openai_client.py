# core/llm/openai_client.py

class OpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Set up openai API client if needed

    def generate_code(self, prompt: str) -> str:
        """
        Mock or real call to OpenAI LLM.
        """
        return f"# [OpenAI generated]\n# Prompt:\n# {prompt}\n\nprint('Hello from OpenAI!')"