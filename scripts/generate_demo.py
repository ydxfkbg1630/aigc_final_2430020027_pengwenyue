from __future__ import annotations
import csv, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.base import ROOT, write_json
from src.story_generator import StoryRequest, generate_story
from src.image_generator import generate_story_images
from src.tts import generate_story_audio
from src.video_maker import make_story_video
from src.agent import run_agent, save_agent_run
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportImage, PageBreak

def build_pdf(story, images, target):
    styles=getSampleStyleSheet(); title=ParagraphStyle('TitleCN', parent=styles['Title'], alignment=TA_CENTER, fontSize=24, leading=32); body=ParagraphStyle('BodyCN', parent=styles['BodyText'], fontSize=12, leading=20)
    doc=SimpleDocTemplate(str(target), pagesize=A4, rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42); flow=[Paragraph(story['title'],title),Paragraph('作者：彭文玥｜多模态儿童故事绘本',body),Spacer(1,18)]
    for scene,image in zip(story['scenes'],images):
        flow += [ReportImage(str(image), width=500, height=375), Paragraph(f"第{scene['scene_id']}幕｜{scene['description']}",styles['Heading2']), Paragraph(scene['text'],body), Spacer(1,18)]
    flow += [Paragraph('故事寓意',styles['Heading2']),Paragraph(story['moral'],body)]; doc.build(flow)

def main():
    ROOT.joinpath('outputs/images').mkdir(parents=True,exist_ok=True); ROOT.joinpath('outputs/audio').mkdir(parents=True,exist_ok=True)
    story=generate_story(StoryRequest()); write_json(ROOT/'outputs/story_structured.json',story)
    images=generate_story_images(story); audio=generate_story_audio(story)
    build_pdf(story,images,ROOT/'outputs/storybook.pdf')
    video,subtitle=make_story_video(story,images,audio.get('narrator'))
    context=run_agent('月光森林里，一封星光信件寻找勇气', ['把主角设定为女孩', '保留森林场景'])
    save_agent_run(context,'case_01')
    context2=run_agent('海边灯塔的合作冒险', ['把场景改成海边'])
    save_agent_run(context2,'case_02')
    write_json(ROOT/'outputs/retrieval/recommendation.json', __import__('src.rag_store',fromlist=['StoryMaterialStore']).StoryMaterialStore().recommend('勇气与友谊的森林冒险'))
    print(json.dumps({'story':str(ROOT/'outputs/story_structured.json'),'images':len(images),'audio':len(audio),'video':str(video),'subtitle':str(subtitle),'storybook':str(ROOT/'outputs/storybook.pdf')},ensure_ascii=False,indent=2))
if __name__=='__main__': main()

