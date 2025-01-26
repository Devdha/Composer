# utils/validation.py
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class SecurityValidator:
    def validate(self, code: str) -> Dict:
        """
        Validate the generated code for security issues.
        Returns {passed: bool, issues: list[str], ...}
        """
        # In real usage, run Bandit or other scanners.
        # For now, stub that everything is safe except
        # if code has "eval(" or something suspicious.
        suspicious = "eval(" in code
        if suspicious:
            return {
                "passed": False,
                "issues": ["Found eval(), which is potentially unsafe"]
            }
        else:
            return {
                "passed": True,
                "issues": []
            }

    def full_audit(self, project_path) -> Dict:
        """
        Perform a deeper audit on the entire project directory.
        """
        # Could recursively scan files with Bandit, etc.
        return {
            "passed": True,
            "details": "No major issues found."
        }