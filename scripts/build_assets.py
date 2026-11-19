from __future__ import annotations
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
def save_json(path, data): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
def main():
    templates=[('星空探险','主角在星空中寻找回家的路，主题勇气与友谊'),('海边灯塔','主角和朋友修复灯塔，主题责任与合作'),('森林邮局','主角为迷路的动物送信，主题善意与坚持'),('云端学校','主角帮助云朵同学完成一次实验，主题好奇与分享'),('时间花园','主角在花园里认识不同季节，主题成长与珍惜'),('月球图书馆','主角整理会发光的故事书，主题阅读与想象'),('彩虹火车','主角和伙伴找回彩虹车票，主题信任与勇敢'),('海底音乐会','主角帮助鲸鱼找到节奏，主题倾听与协作'),('机器人早餐店','主角教机器人做早餐，主题耐心与创造'),('风筝山谷','主角让风筝带着愿望飞翔，主题希望与行动')]
    for i,(title,desc) in enumerate(templates,1): save_json(ROOT/f'data/templates/template_{i:02d}.json',{'id':i,'title':title,'description':desc})
    chars=[('云朵兔','温柔、谨慎','白色长耳朵兔子，淡蓝色星纹，橙色围巾'),('星光鲸','沉稳、善良','蓝色小鲸鱼，银色星点，月牙尾巴'),('机械小鹿','认真、细心','银色机械鹿，绿色眼睛，背着工具包'),('彩虹狐','活泼、热心','橙色狐狸，彩虹尾巴，蓝色小帽子'),('月影猫','安静、聪明','深灰色猫，月牙耳饰，紫色围巾'),('风铃鸟','开朗、敏捷','青色小鸟，翅膀像风铃，黄色脚环')]
    for i,(name,traits,appearance) in enumerate(chars,1): save_json(ROOT/f'data/characters/character_{i:02d}.json',{'name':name,'traits':traits,'appearance':appearance})
    scenes=[('月光森林','月光穿过树叶，银色小路通向邮局'),('雾桥','白雾覆盖的木桥，桥下有发光水流'),('星光湖','平静湖面映照北斗星，水边有芦苇'),('云端教室','漂浮的教室，窗外是柔软云海'),('海边灯塔','海风吹过红白灯塔，远处有帆船'),('月球书库','圆顶书库里漂浮着发光书页'),('彩虹车站','七色轨道穿过山谷，站台有风铃'),('海底剧场','珊瑚搭成的舞台，气泡漂向海面'),('机器人厨房','彩色锅具和会发光的烤箱'),('风筝山谷','高山之间飘着不同形状的风筝')]
    for i,(name,desc) in enumerate(scenes,1): save_json(ROOT/f'data/scenes/scene_{i:02d}.json',{'name':name,'description':desc})
    sounds=[('forest_night','森林夜晚环境音'),('magic_chime','星光铃声'),('water_ripple','湖水波纹'),('wind_breeze','山谷微风'),('page_turn','翻书声音')]
    for i,(name,desc) in enumerate(sounds,1): save_json(ROOT/f'data/sounds/sound_{i:02d}.json',{'name':name,'description':desc,'license':'free_demo_placeholder'})
    image_dir=ROOT/'data/images'; image_dir.mkdir(parents=True,exist_ok=True)
    for i in range(1,21):
        image=Image.new('RGB',(640,420),(14+(i*7)%80,30+(i*11)%80,72+(i*13)%100)); draw=ImageDraw.Draw(image)
        for j in range(8):
            x=(j*83+i*17)%620; y=(j*47+i*23)%380; draw.ellipse((x,y,x+10,y+10),fill=(255,235,150))
        draw.rounded_rectangle((35,300,605,385),radius=20,fill=(35,72,124),outline=(112,204,255),width=3)
        draw.text((60,325),f'故事素材图 {i:02d}',fill='white')
        image.save(image_dir/f'image_{i:02d}.png')
if __name__=='__main__': main()
