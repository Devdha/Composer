import logging
from typing import Dict, Optional
from pathlib import Path
from .planner import Planner
from .code_generator import CodeGenerator
from .test_runner import TestRunner
from .debugger import Debugger
from .knowledge_base import KnowledgeBase
from utils.validation import SecurityScanner
from utils.file_manager import FileManager
from config.settings import MAX_RETRIES, ALLOWED_TECH

class AutonomousCoder:
    def __init__(self, llm_api_key: str):
        self.planner = Planner(llm_api_key)
        self.code_gen = CodeGenerator(llm_api_key)
        self.test_runner = TestRunner()
        self.debugger = Debugger(llm_api_key)
        self.file_manager = FileManager()
        self.knowledge_base = KnowledgeBase()
        self.security = SecurityScanner()
        self.logger = logging.getLogger(__name__)

    def build_service(self, user_prompt: str) -> Dict:
        try:
            # Phase 1: Requirement Analysis
            clarity_check = self.planner.analyze_ambiguity(user_prompt)
            if clarity_check['needs_clarification']:
                return {
                    'status': 'clarification_needed',
                    'questions': clarity_check['questions']
                }

            # Phase 2: Architecture Planning
            development_plan = self.planner.create_plan(
                user_prompt,
                tech_constraints=ALLOWED_TECH
            )
            self._validate_plan(development_plan)

            # Phase 3: Project Initialization
            project_path = self.file_manager.create_project(
                development_plan['metadata']['project_name']
            )
            self.file_manager.save_plan(project_path, development_plan)

            # Phase 4: Iterative Development
            for step in development_plan['steps']:
                self._execute_development_step(step, project_path)

            # Phase 5: Security Audit
            audit_result = self.security.scan_project(project_path)
            if not audit_result['passed']:
                self._handle_security_issues(audit_result, project_path)

            return {'status': 'success', 'path': str(project_path)}

        except Exception as e:
            self.logger.error(f"Build failed: {str(e)}")
            return {'status': 'failed', 'error': str(e)}

    def _execute_development_step(self, step: Dict, project_path: Path):
        for attempt in range(MAX_RETRIES):
            # Code Generation
            context = self.knowledge_base.get_context(step['type'])
            code = self.code_gen.generate(
                step['description'],
                context=context
            )
            
            # Security Validation
            if self.security.detect_vulnerabilities(code):
                code = self.debugger.fix_security_issues(code)
                
            # Write Code
            self.file_manager.write_code(
                project_path,
                code,
                filename=step.get('output_file', 'main.py')
            )

            # Test Execution
            test_result = self.test_runner.run_tests(project_path)
            if test_result['passed']:
                self.knowledge_base.store_solution(step['type'], code)
                break

            # Debugging Cycle
            code = self.debugger.fix_code(
                code,
                test_result['errors'],
                project_context=self.file_manager.read_plan(project_path)
            )
        else:
            raise RuntimeError(f"Failed step: {step['description']}")

    def _validate_plan(self, plan: Dict):
        required_keys = {'metadata', 'steps', 'dependencies'}
        if not required_keys.issubset(plan.keys()):
            raise ValueError("Invalid development plan structure")