# core/planner.py
import yaml
from typing import Dict, List
from core.llm.prompt import Prompt
from core.llm.deepseek_client import DeepSeekClient
from utils.parser import parse_llm_output
import logging
import os


class Planner:
    """
    Combines all planning functionalities:
    - Analyzing ambiguity in requirements
    - Generating architecture and tech plans in YAML
    - Structuring plans with resolved dependencies
    """

    def __init__(self, llm_client: DeepSeekClient):
        self.client = llm_client
        self.logger = logging.getLogger(__name__)
        self.required_components = {
            'web_service': ['database', 'auth', 'api'],
            'cli_tool': ['argument_parsing', 'file_io']
        }

    def analyze_ambiguity(self, prompt: str) -> Dict:
        """
        Analyze technical requirements to identify ambiguities.
        Returns JSON with 'needs_clarification' and a list of 'questions'.
        """
        system_msg = """Analyze technical requirements. Identify:
        1. Unspecified components
        2. Missing technical specifications
        3. Potential contradictions
        Output JSON format: {"needs_clarification": bool, "questions": List[str]}
        Don't show markdown code block in the response. Just return the formatted data.
        """

        try:
            prompt_obj = Prompt()
            prompt_obj.add_system_message(system_msg)
            prompt_obj.add_user_message(prompt)
            response = self.client.generate_code(prompt_obj)
            return parse_llm_output(response)
        except Exception as e:
            self.logger.error(f"Error analyzing ambiguity: {str(e)}", exc_info=True)
            raise

    def create_tech_plan(self, requirements: str) -> Dict:
        """
        Generate a high-level tech plan in YAML format.
        The plan includes:
        - Optimal tech stack
        - Architecture design
        - Potential risks
        """
        system_msg = """As a senior architect, analyze requirements and:
        1. Choose optimal tech stack
        2. Design architecture
        3. Identify potential risks
        Use YAML format with technical details.
        Don't show markdown code block in the response. Just return the formatted data.
        """

        try:
            prompt_obj = Prompt()
            prompt_obj.add_system_message(system_msg)
            prompt_obj.add_user_message(requirements)
            response = self.client.generate_code(prompt_obj)
            raw_plan = self._sanitize_response(response)
            return self._parse_plan(raw_plan)
        except Exception as e:
            self.logger.error(f"Error creating tech plan: {str(e)}", exc_info=True)
            raise

    def create_plan(self, requirements: str) -> Dict:
        """
        Generate a complete project plan in YAML format, including:
        - Optimal tech stack selection
        - Justification for each choice
        """
        system_msg = """
        Autonomously select the optimal tech stack considering:
        1. Project complexity
        2. Team skill level (assume senior engineers)
        3. Community support
        4. Cloud-native capabilities
        
        Generate a complete project plan in YAML format that MUST include these required fields:      
        
        project: <project_name>
        directory_structure:
          # Must be a dictionary where keys are folder names and values are lists of files
          src:
            - list of files in src
          tests:
            - list of files in tests
          # Add other folders as needed
        
        components:
          - name: <component_name>
            description: <component_requirements>
        
        tech_stack:
          - List of technologies and versions
        
        The directory_structure MUST be a dictionary where each key is a folder name and its value is a list of files.
        Example directory_structure:
          src: 
            - __init__.py
            - main.py
          tests:
            - test_main.py
        
        The plan must include ALL these fields as they are required by the build system.
        Additional fields can be included but these are mandatory.
        Don't show markdown code block in the response. Just return the formatted data.
        """

        try:
            prompt_obj = Prompt()
            prompt_obj.add_system_message(system_msg)
            prompt_obj.add_user_message(requirements)
            response = self.client.generate_code(prompt_obj)
            self.logger.info(f"Generated plan: {response}")
            
            sanitized_response = self._sanitize_response(response)
            plan = self._parse_plan(sanitized_response)
            
            self._save_plan_to_file(plan, "latest_plan.yaml")
            self.logger.info("Generated Plan:\n" + yaml.dump(plan, default_flow_style=False))
            
            return plan
        except Exception as e:
            self.logger.error(f"Error creating plan: {str(e)}", exc_info=True)
            raise

    def _sanitize_response(self, response: str) -> str:
        """
        Sanitize the response to ensure it is valid YAML.
        """
        sanitized = response.replace("```yaml", "").replace("```", "").strip()
        return sanitized

    def _parse_plan(self, raw_plan: str) -> Dict:
        """
        Parse a raw YAML plan text into a Python dictionary and apply additional processing.
        """
        try:
            lines = raw_plan.split("\n")
            lines = [line for line in lines if not line.strip().startswith("```yaml") and not line.strip().startswith("```") and not line.strip().startswith("---")]
            raw_plan = "\n".join(lines)
            plan = yaml.safe_load(raw_plan)
            if "metadata" not in plan:
                plan["metadata"] = {}
            plan["metadata"]["version"] = "1.0.0"

            plan["dependencies"] = self._resolve_dependencies(plan.get("technology_stack", []))
            return plan
        except yaml.YAMLError as e:
            self.logger.error(f"YAML parsing error: {str(e)}", exc_info=True)
            raise ValueError(f"Invalid plan format: {str(e)}")

    def _resolve_dependencies(self, tech_stack: List[str]) -> Dict:
        """
        Resolve dependencies dynamically for the given tech stack.
        """
        return {
            "resolved_dependencies": [f"{tech}-1.0.0" for tech in tech_stack]
        }

    def _save_plan_to_file(self, plan: Dict, filename: str):
        """
        Save the plan to a YAML file.
        """
        try:
            with open(filename, 'w') as file:
                yaml.dump(plan, file, default_flow_style=False)
            self.logger.info(f"Plan saved to {filename}")
        except IOError as e:
            self.logger.error(f"Failed to save plan to file: {str(e)}", exc_info=True)
            raise
