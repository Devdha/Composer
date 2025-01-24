from .llm_client import DeepSeekClient

class Debugger:
    def __init__(self, api_key: str):
        self.client = DeepSeekClient(api_key)
    
    def resolve_issue(self, error_data: dict) -> str:
        context = f"""
        Tech Stack: {error_data['tech_stack']}
        Error: {error_data['error']}
        Code Snippet: {error_data['code']}
        """
        
        return self.client.generate(
            prompt_type="debugging",
            messages=[
                {"role": "system", "content": "Diagnose and fix technical issues"},
                {"role": "user", "content": context}
            ]
        )