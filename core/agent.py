import json
import yaml
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from utils.files import ProjectManager
from utils.validation import SecurityValidator
from utils.test_runner import TestRunner
from core.planner import Planner
from core.coder import CodeGenerator
from core.debugger import DebugEngine
from core.knowledge import KnowledgeBase

logger = logging.getLogger(__name__)

class Composer:
    def __init__(
        self,
        llm_client: Any,
        output_dir: Path = Path("services"),
        config_path: Path = Path("config/settings.yaml")
    ):
        self.llm = llm_client
        self.output_dir = output_dir
        self.project_manager = ProjectManager()
        self.security = SecurityValidator()
        self.test_runner = TestRunner()
        self.knowledge = KnowledgeBase()
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        # Initialize components
        self.planner = Planner(self.llm)
        self.coder = CodeGenerator(self.llm)
        self.debugger = DebugEngine(self.llm)
        
        # State tracking
        self.current_project: Optional[Path] = None
        self.iteration_count = 0
        self.error_history = []

    def build_service(self, requirements: str) -> Dict[str, Any]:
        """Full service build lifecycle"""
        project_path = None
        try:
            self.logger.info("Starting requirement analysis and planning")
            tech_plan = self.planner.create_plan(
                requirements
            )
            
            self.logger.info("Initializing project")
            project_path = self._init_project(tech_plan)
            self.current_project = project_path
            
            # Save plan immediately after initialization
            self._save_build_state(project_path, {
                "timestamp": datetime.now().isoformat(),
                "requirements": requirements,
                "tech_plan": tech_plan,
                "status": "in_progress"
            })
            
            self.logger.info("Starting iterative development")
            for component in tech_plan["components"]:
                self._execute_development_step(
                    component=component,
                    tech_stack=tech_plan["tech_stack"],
                    project_path=project_path
                )
            
            self.logger.info("Running final validation")
            final_result = self._final_validation(project_path)
            
            self.logger.info("Updating knowledge base")
            self.knowledge.store_project(
                project_path=project_path,
                plan=tech_plan,
                error_history=self.error_history
            )
            
            return {
                "status": "success",
                "path": str(project_path),
                "iterations": self.iteration_count,
                "warnings": final_result.get("warnings", [])
            }
            
        except Exception as e:
            self.logger.error(f"Error during service build: {str(e)}", exc_info=True)
            if project_path:
                # Update build state with error instead of deleting
                self._save_build_state(project_path, {
                    "timestamp": datetime.now().isoformat(),
                    "status": "failed",
                    "error": str(e),
                    "iterations": self.iteration_count,
                    "error_history": self.error_history
                })
            return {
                "status": "error",
                "error": str(e),
                "iterations": self.iteration_count,
                "errors": self.error_history,
                "path": str(project_path) if project_path else None
            }

    def _init_project(self, tech_plan: Dict) -> Path:
        """Initialize project structure"""
        project_name = tech_plan["project"]
        project_path = self.output_dir / project_name
        
        # Create directory structure
        self.project_manager.create(
            path=project_path,
            structure=tech_plan["directory_structure"]
        )
        
        # Save technical plan
        with open(project_path / "tech_plan.yaml", "w") as f:
            yaml.dump(tech_plan, f)
            
        return project_path

    def _execute_development_step(
        self,
        component: Dict,
        tech_stack: Dict,
        project_path: Path,
        max_retries: int = 5
    ):
        """Iterative development of a single component"""
        for attempt in range(max_retries):
            self.iteration_count += 1
            
            # Generate initial code
            code = self.coder.generate(
                requirements=component["description"],
                tech_stack=tech_stack,
                previous_errors=self.error_history[-3:]  # Last 3 errors
            )
            
            # Security validation
            security_report = self.security.validate(code)
            if not security_report["passed"]:
                # Attempt to fix security issues
                code = self.debugger.fix_security_issues(
                    code,
                    issues=security_report["issues"],
                    context=tech_stack
                )
                
            # Save code version
            version_path = self.project_manager.write_code(
                project_path=project_path,
                component_name=component["name"],
                code=code,
                iteration=self.iteration_count
            )
            
            # Run automated tests
            test_result = self.test_runner.execute(
                project_path=project_path,
                component=component["name"]
            )
            
            if test_result["passed"]:
                # If tests passed, store success in knowledge
                self.knowledge.store_success(
                    component=component["name"],
                    code=code,
                    context=tech_stack
                )
                return  # Done with this component
                
            # Handle test failure
            self.error_history.append({
                "iteration": self.iteration_count,
                "component": component["name"],
                "error": test_result["error"],
                "logs": test_result["logs"]
            })
            
            # Debug and improve code
            code = self.debugger.fix(
                code=code,
                error_context=test_result,
                tech_stack=tech_stack,
                knowledge_base=self.knowledge
            )
            
        raise RuntimeError(
            f"Failed to implement '{component['name']}' after {max_retries} attempts"
        )

    def _final_validation(self, project_path: Path) -> Dict:
        """Run final security and quality checks"""
        report = {
            "security": self.security.full_audit(project_path),
            "tests": self.test_runner.run_all(project_path),
            "style": self.project_manager.check_style(project_path)
        }
        
        if not report["security"]["passed"]:
            raise RuntimeError("Security validation failed")
            
        if not report["tests"]["all_passed"]:
            raise RuntimeError("Final test suite failed")
            
        return report

    def _save_build_state(self, project_path: Path, state: Dict[str, Any]):
        """Save build state to the project directory"""
        build_state_path = project_path / "build_state.json"
        with open(build_state_path, "w") as f:
            json.dump(state, f, indent=2)

    def _cleanup_failed_project(self):
        """Method kept for compatibility but now just logs the failure"""
        if self.current_project and self.current_project.exists():
            logger.warning(f"Build failed for project: {self.current_project}")