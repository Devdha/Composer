# config/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

DEEPSEEK_CONFIG = {
    "api_key": os.getenv("DEEPSEEK_API_KEY"),
    "base_url": "https://api.deepseek.com/v1",
    "models": {
        "coding": "deepseek-coder-33b-instruct",
        "planning": "deepseek-chat-32k"
    }
}

TECH_CONSTRAINTS = {
    "banned_tech": ["COBOL", "VB6"],
    "preferred_cloud": "AWS"
}