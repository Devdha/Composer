import unittest
from unittest.mock import Mock
from composer.core.agent import Composer
from composer.utils.file_manager import FileManager

class TestComposer(unittest.TestCase):
    def setUp(self):
        self.mock_llm = Mock()
        self.agent = Composer(llm_api_key="mock-key")
        self.agent.planner = Mock()
        
    def test_project_creation(self):
        self.agent.planner.create_plan.return_value = {
            "project_name": "test",
            "steps": []
        }
        result = self.agent.build_service("Test project")
        self.assertEqual(result['status'], 'success')
        self.assertTrue(FileManager().project_exists("test"))