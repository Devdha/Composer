import yaml
from typing import Dict, List
from openai import OpenAI
from utils.parser import parse_llm_output
from config.settings import DEFAULT_TECH_STACK
from core.llm_client import DeepSeekClient

class Planner:
    def __init__(self, api_key: str):
        self.client = DeepSeekClient(api_key)
        self.required_components = {
            'web_service': ['database', 'auth', 'api'],
            'cli_tool': ['argument_parsing', 'file_io']
        }

    def analyze_ambiguity(self, prompt: str) -> Dict:
        system_msg = """Analyze technical requirements. Identify:
        1. Unspecified components
        2. Missing technical specifications
        3. Potential contradictions
        Output JSON format: {"needs_clarification": bool, "questions": List[str]}"""
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return parse_llm_output(response.choices[0].message.content)
    
    from .llm_client import DeepSeekClient
from utils.parser import parse_yaml

class Planner:
    def __init__(self, api_key: str):
        self.client = DeepSeekClient(api_key)
    
    def create_tech_plan(self, requirements: str) -> dict:
        system_msg = """As a senior architect, analyze requirements and:
        1. Choose optimal tech stack
        2. Design architecture
        3. Identify potential risks
        Use YAML format with technical details"""
        
        response = self.client.generate(
            prompt_type="planning",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": requirements}
            ]
        )
        return parse_yaml(response)

    def create_plan(self, prompt: str) -> Dict:
      system_msg = """Autonomously select the optimal tech stack considering:
      1. Project complexity
      2. Team skill level (assume senior engineers)
      3. Community support
      4. Cloud-native capabilities
      Output YAML with justification for each choice"""
      
      response = self.client.chat.completions.create(
          model="gpt-4-turbo",
          messages=[
              {"role": "system", "content": system_msg},
              {"role": "user", "content": prompt}
          ],
          temperature=0.7  # Higher creativity
      )
      return self._parse_plan(response.choices[0].message.content)

    def _structure_plan(self, raw_plan: str) -> Dict:
        try:
            plan = yaml.safe_load(raw_plan)
            plan['metadata']['version'] = "1.0.0"
            plan['dependencies'] = self._resolve_dependencies(plan['technology_stack'])
            return plan
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid plan format: {str(e)}")

    def _resolve_dependencies(self, tech_stack: List[str]) -> Dict:
        # Integrated with actual package databases
        return {
            'python': [
                pypi_mirror.get_latest_version(tech)
                for tech in tech_stack if tech in pypi_mirror
            ]
        }