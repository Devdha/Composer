# core/coder.py
from core.llm.prompt import Prompt

class CodeGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def generate(self, requirements: str, tech_stack: dict, previous_errors=None) -> str:
        system_msg = f"""
        You are a programming expert. Write production-grade code that:

        1. Implements exactly: {requirements}
        2. Uses {tech_stack} framework
        3. Includes error handling
        4. Has type hints (if applicable)
        5. Avoids security vulnerabilities:
          - SQL injection
          - XSS
          - Insecure deserialization
          - Hardcoded secrets
        6. Includes TODO comments for complex sections

        Output ONLY the code with brief inline comments. Never explain outside code.
        And the code only contains the code, no other text(ex. markdown, etc.).

        Example structure:
        # Imports here
        # Main functionality
        # Unit test stubs
        """
        user_msg = f"""
        Requirements: {requirements}
        Tech stack: {tech_stack}
        Previous errors: {previous_errors}
        """

        prompt_obj = Prompt()
        prompt_obj.add_system_message(system_msg)
        prompt_obj.add_user_message(user_msg)

        response = self.llm.generate_code(prompt_obj)
        return response