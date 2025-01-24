import json
import yaml
from typing import Any

def parse_llm_output(output: str) -> Any:
    try:
        if output.strip().startswith("{"):
            return json.loads(output)
        elif "---" in output:  # YAML format
            return yaml.safe_load(output)
        return output
    except Exception as e:
        raise ValueError(f"LLM output parsing failed: {str(e)}")