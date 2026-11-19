import unittest
from src.agent import plan
class AgentTest(unittest.TestCase):
    def test_intervention_changes_plan(self):
        self.assertIn('apply_user_intervention', plan('海边故事',['改成女孩']))
        self.assertEqual(plan('故事'),['retrieve_materials','write_structured_story','generate_images','synthesize_audio','make_video'])
if __name__=='__main__': unittest.main()
