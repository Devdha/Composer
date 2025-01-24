import subprocess
from typing import Dict

class TestRunner:
    def run(self, project_path: str) -> Dict:
        try:
            result = subprocess.run(
                ["pytest", f"{project_path}/tests"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "error_log": result.stderr,
                "stdout": result.stdout
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error_log": "Test execution timed out."}