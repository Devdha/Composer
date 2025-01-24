import os
from pathlib import Path

# config/settings.py
LLM_PROVIDER = "deepseek"  # Switch to "openai" or others
LLM_CONFIG = {
    "deepseek": {
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "model": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com/v1"
    },
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-4o",
        "base_url": "https://api.openai.com/v1"
    }
}

# Core configuration
MAX_RETRIES = 3
PROJECT_ROOT = Path(__file__).parent.parent
TECH_POLICY = {
    "criteria": [
        "Choose the most appropriate stack based on requirements",
        "Prioritize modern, well-supported technologies",
        "Ensure components are compatible"
    ]
}

# LLM Configuration
DEFAULT_MODEL = "gpt-4-turbo"
TEMPERATURE_MAP = {
    "planning": 0.2,
    "coding": 0.5,
    "debugging": 0.7
}

# Security
BANNED_PATTERNS = [
    r"os\.system\(",
    r"subprocess\.run\(",
    r"exec\(",
    r"eval\("
]