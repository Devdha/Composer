# utils/files.py
import os
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ProjectManager:
    def create(self, path: Path, structure: Dict[str, Any]):
        """
        Create the directory structure based on a dictionary like:
            {
              "src": ["__init__.py", "main.py"],
              "tests": ["test_main.py"]
            }
        """
        path.mkdir(parents=True, exist_ok=True)
        for folder_name, files in structure.items():
            folder_path = path / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            for filename in files:
                file_path = folder_path / filename
                if not file_path.exists():
                    file_path.touch()
        logger.info(f"Initialized project structure at {path}")

    def write_code(self, project_path: Path, component_name: str, code: str, iteration: int) -> Path:
        """
        Write code to a component-specific folder, versioned by iteration.
        E.g.  <project_path>/<component_name>/iteration_<n>/main.py
        """
        comp_path = project_path / component_name / f"iteration_{iteration}"
        comp_path.mkdir(parents=True, exist_ok=True)
        main_file = comp_path / "main.py"
        
        with open(main_file, "w", encoding="utf-8") as f:
            f.write(code)
        
        logger.info(f"Wrote code for {component_name} (iteration {iteration}) to {main_file}")
        return comp_path

    def check_style(self, project_path: Path):
        """
        Placeholder for style/lint checks.
        Could call flake8 or black here. We just return a stub.
        """
        # Suppose everything is fine:
        return {
            "passed": True,
            "warnings": []
        }