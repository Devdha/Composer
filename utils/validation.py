import re
from typing import Dict

class SecurityScanner:
    def __init__(self):
        self.banned_patterns = [
            r"os\.system\(",
            r"subprocess\.run\(",
            r"exec\(",
            r"eval\("
        ]

    def validate_code(self, code: str) -> Dict:
        results = {
            "security_issues": [],
            "syntax_valid": True
        }
        
        # Pattern checks
        for pattern in self.banned_patterns:
            if re.search(pattern, code):
                results["security_issues"].append(
                    f"Dangerous pattern detected: {pattern}"
                )
                
        # Syntax validation
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as e:
            results["syntax_valid"] = False
            results["syntax_error"] = str(e)
            
        return results