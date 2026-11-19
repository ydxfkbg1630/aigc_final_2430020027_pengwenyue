import unittest
from pathlib import Path
from src.story_generator import StoryRequest, generate_story, validate_story
from src.rag_store import StoryMaterialStore
class StoryPipelineTest(unittest.TestCase):
    def test_story_schema(self):
        story=generate_story(StoryRequest())
        self.assertEqual(len(story['characters']),3); self.assertEqual(len(story['scenes']),3); validate_story(story)
    def test_material_counts(self):
        root=Path(__file__).resolve().parents[1]/'data'
        self.assertGreaterEqual(len(list((root/'templates').glob('*.json'))),10)
        self.assertGreaterEqual(len(list((root/'images').glob('*.png'))),20)
        self.assertGreaterEqual(len(list((root/'sounds').glob('*.json'))),5)
    def test_retrieval(self):
        result=StoryMaterialStore().recommend('森林勇气冒险')
        self.assertIn('template_ids',result); self.assertTrue(result['results'])
if __name__=='__main__': unittest.main()
