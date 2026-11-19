from __future__ import annotations
import urllib.parse, urllib.request
from pathlib import Path
from .base import ROOT, load_env, stable_seed

def _fallback_image(path: Path, title: str, prompt: str, scene_id: int) -> Path:
    from PIL import Image, ImageDraw, ImageFont
    image=Image.new('RGB',(1024,768),(22+scene_id*8,38+scene_id*12,86+scene_id*14)); draw=ImageDraw.Draw(image)
    font_path='C:/Windows/Fonts/msyh.ttc'; font=ImageFont.truetype(font_path,28) if Path(font_path).exists() else ImageFont.load_default(); small=ImageFont.truetype(font_path,20) if Path(font_path).exists() else ImageFont.load_default()
    for x,y in [(120,110),(260,180),(420,90),(620,150),(840,110),(920,260),(180,320),(520,280)]: draw.ellipse((x,y,x+12,y+12),fill=(255,231,142))
    draw.ellipse((730,70,890,230),fill=(248,238,181))
    draw.rounded_rectangle((85,390,420,690),radius=45,fill=(75,145,230),outline=(197,235,255),width=5)
    draw.ellipse((145,290,365,500),fill=(255,224,190),outline=(39,49,100),width=4)
    draw.arc((180,390,330,475),0,180,fill=(50,35,70),width=5); draw.ellipse((205,360,220,375),fill=(35,45,75)); draw.ellipse((290,360,305,375),fill=(35,45,75)); draw.polygon([(280,305),(310,270),(340,315)],fill=(255,224,55))
    draw.ellipse((470,490,760,650),fill=(245,245,250),outline=(126,195,255),width=5); draw.ellipse((520,420,620,540),fill=(245,245,250),outline=(126,195,255),width=5); draw.ellipse((515,360,550,450),fill=(245,245,250),outline=(126,195,255),width=4); draw.ellipse((590,360,625,450),fill=(245,245,250),outline=(126,195,255),width=4); draw.ellipse((545,470,560,485),fill=(35,45,75)); draw.ellipse((585,470,600,485),fill=(35,45,75))
    draw.rounded_rectangle((60,30,964,100),radius=25,fill=(16,27,65),outline=(160,220,255),width=3); draw.text((90,51),f'{title} · 免费生图演示',font=font,fill='white')
    draw.rounded_rectangle((55,690,969,745),radius=18,fill=(16,27,65)); draw.text((78,706),f'角色锚点与seed保持一致｜场景 {scene_id}',font=small,fill=(220,241,255))
    path.parent.mkdir(parents=True,exist_ok=True); image.save(path); return path

def generate_image(prompt: str, output_path: Path, seed: int | None = None, width: int = 1024, height: int = 768) -> Path:
    env=load_env(); seed=seed if seed is not None else stable_seed(prompt); use_remote=env.get('USE_REMOTE_IMAGES','0').lower() in {'1','true','yes'}
    if not use_remote: return _fallback_image(output_path,'故事星球',prompt,seed%3+1)
    base=env.get('POLLINATIONS_BASE_URL','https://image.pollinations.ai/prompt').rstrip('/'); encoded=urllib.parse.quote(prompt,safe=''); url=f'{base}/{encoded}?width={width}&height={height}&seed={seed}&nologo=true'
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'AIGC-Story-Workshop/1.0'})
        with urllib.request.urlopen(request,timeout=90) as response: payload=response.read()
        if not (payload.startswith(b'\x89PNG') or payload.startswith(b'\xff\xd8')): raise ValueError('生图接口返回内容类型异常')
        output_path.parent.mkdir(parents=True,exist_ok=True); output_path.write_bytes(payload); return output_path
    except Exception: return _fallback_image(output_path,'故事星球',prompt,seed%3+1)

def generate_story_images(story: dict, output_dir: Path | None = None) -> list[Path]:
    output_dir=output_dir or ROOT/'outputs/images'; output_dir.mkdir(parents=True,exist_ok=True); anchor='同一角色锚点：10岁东亚女孩，黑色齐肩短发，黄色星星发夹，蓝色连帽外套，红色小背包；白色长耳朵云朵兔，橙色围巾；儿童绘本，柔和水彩，角色比例统一'; paths=[]
    for scene in story['scenes']:
        prompt=f'{anchor}；{scene["visual_prompt"]}；场景{scene["scene_id"]}；画面干净，适合7到12岁儿童阅读'; paths.append(generate_image(prompt,output_dir/f'scene_{scene["scene_id"]:02d}.png',stable_seed(anchor+str(scene['scene_id'])),1024,768))
    return paths
