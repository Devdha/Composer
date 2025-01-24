# composer.py
from core import Planner, CodeGenerator, Debugger
from config import settings

class Composer:
    def __init__(self, api_key: str):
        self.planner = Planner(api_key)
        self.coder = CodeGenerator(api_key)
        self.debugger = Debugger(api_key)
        # ... rest of initialization
    
    def build_service(self, prompt: str):
        # Full autonomous flow using DeepSeek models
        tech_plan = self.planner.create_tech_plan(prompt)
        # ... rest of implementation