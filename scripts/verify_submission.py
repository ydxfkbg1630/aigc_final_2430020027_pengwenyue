from __future__ import annotations
import hashlib, json, re, sys, zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.base import ROOT, read_json

def main():
    required=['README.md','requirements.txt','.env.example','src/story_generator.py','src/image_generator.py','src/tts.py','src/video_maker.py','src/rag_store.py','src/agent.py','web/index.html','docs/ai_log.md','outputs/story_structured.json','outputs/storybook.pdf','outputs/video/story_video.mp4']
    missing=[item for item in required if not (ROOT/item).exists()]
    story=read_json(ROOT/'outputs/story_structured.json',{})
    images=list((ROOT/'outputs/images').glob('*.png')); image_assets=list((ROOT/'data/images').glob('*.png')); templates=list((ROOT/'data/templates').glob('*.json')); sounds=list((ROOT/'data/sounds').glob('*.json'))
    leaks=[]
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.md','.py','.json','.html','.csv'}:
            text=path.read_text(encoding='utf-8',errors='ignore')
            legacy_name='\u53f6\u5fb7\u7965'
            if legacy_name in text and path.name != 'verify_submission.py': leaks.append(str(path.relative_to(ROOT)))
    zip_path=ROOT/'AIGC_彭文玥_2430020027_提交包.zip'
    with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in ROOT.rglob('*'):
            if path.is_file() and path.name != zip_path.name and '.git' not in path.parts and '.venv' not in path.parts:
                archive.write(path, path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(zip_path) as archive: crc=archive.testzip() is None; members=len(archive.namelist())
    report={'required_missing':missing,'story_fields':all(k in story for k in ['title','characters','scenes','moral']),'story_characters':len(story.get('characters',[])),'story_scenes':len(story.get('scenes',[])),'generated_images':len(images),'image_assets':len(image_assets),'templates':len(templates),'sounds':len(sounds),'name_leaks':leaks,'zip_crc_ok':crc,'zip_members':members,'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest()}
    (ROOT/'outputs/reports/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(1 if missing or leaks or not crc else 0)
if __name__=='__main__': main()

