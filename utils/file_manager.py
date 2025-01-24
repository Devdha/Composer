from pathlib import Path
import yaml

class FileManager:
    def create_project(self, project_name: str) -> Path:
        path = Path(f"services/{project_name}")
        path.mkdir(parents=True, exist_ok=True)
        (path / "src").mkdir(exist_ok=True)
        (path / "tests").mkdir(exist_ok=True)
        return path

    def save_plan(self, project_path: Path, plan: Dict) -> None:
        with open(project_path / "plan.yaml", "w") as f:
            yaml.dump(plan, f)

    def write_code(self, project_path: Path, code: str) -> None:
        with open(project_path / "src/main.py", "w") as f:
            f.write(code)