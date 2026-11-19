from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.base import ROOT, read_json
from src.video_maker import make_slideshow
from src.tts import generate_story_audio, generate_background_music

def main():
    story=read_json(ROOT/'outputs/story_structured.json')
    audio=generate_story_audio(story)
    scene=sorted((ROOT/'outputs/images').glob('scene_*.png'))
    assets=sorted((ROOT/'data/images').glob('image_*.png'))
    music=generate_background_music(ROOT/'outputs/audio/background_music_long.mp3', 480)
    make_slideshow(scene*5,audio['narrator'],ROOT/'outputs/video/homework0_demo.mp4',seconds_per_image=8,background_audio=music)
    make_slideshow((scene+assets)[:20],audio['narrator'],ROOT/'outputs/video/final_demo.mp4',seconds_per_image=24,background_audio=music)
    print('presentation media generated')
if __name__=='__main__': main()
