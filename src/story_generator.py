from __future__ import annotations
import json, re, urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from .base import ROOT, load_env, write_json
SCHEMA = {"title": "故事标题", "characters": [{"name": "角色名", "traits": "性格特征", "appearance": "外貌描述"}], "scenes": [{"scene_id": 1, "description": "场景描述", "text": "该场景故事文本", "mood": "情绪基调", "visual_prompt": "适合文生图的Prompt"}], "moral": "故事寓意"}
@dataclass
class StoryRequest:
    protagonist: str = "彭文玥"
    protagonist_age: int = 10
    interest: str = "星空观察"
    setting: str = "月光森林"
    theme: str = "勇气与友谊"
    length: str = "中篇"
    audience_age: str = "7-12岁"
def demo_story(request: StoryRequest) -> dict[str, Any]:
    hero = request.protagonist
    return {"title": f"{hero}和月光森林的星星邮局", "characters": [{"name": hero, "traits": "好奇、勇敢、愿意帮助朋友", "appearance": "10岁东亚女孩，黑色齐肩短发，黄色星星发夹，蓝色连帽外套，红色小背包，圆眼睛"}, {"name": "云朵兔", "traits": "温柔、谨慎、善于发现线索", "appearance": "白色长耳朵兔子，耳尖有淡蓝色星纹，戴橙色围巾"}, {"name": "星光鲸", "traits": "沉稳、善良、会发出柔和蓝光", "appearance": "小小的蓝色星光鲸，背上有银色星点，尾巴像月牙"}], "scenes": [{"scene_id": 1, "description": f"{request.setting}的邮局门口，夜空落下了一封会发光的信", "text": f"{hero}在{request.setting}观察星空时，看见一封银色信件从云层飘来。信封上写着：请把勇气送到迷路的星光鲸那里。", "mood": "神秘而温暖", "visual_prompt": "月光森林，银色星星邮局，10岁东亚女孩，黑色齐肩短发，黄色星星发夹，蓝色连帽外套，红色小背包，白色云朵兔，儿童绘本，柔和水彩，统一角色外观"}, {"scene_id": 2, "description": "雾桥旁，云朵兔和主角寻找发光脚印", "text": f"{hero}和云朵兔沿着发光脚印走到雾桥。桥下传来轻轻的歌声，他们决定牵着手一起走过去。", "mood": "紧张又坚定", "visual_prompt": "月光森林雾桥，10岁东亚女孩，黑色齐肩短发，黄色星星发夹，蓝色连帽外套，红色小背包，白色云朵兔，发光脚印，儿童绘本，柔和水彩，统一角色外观"}, {"scene_id": 3, "description": "湖面上，星光鲸重新找到回家的方向", "text": f"{hero}把信件交给星光鲸，云朵兔用耳朵指向北方最亮的星。星光鲸跃出湖面，蓝色光点组成一条回家的路。", "mood": "明亮而感动", "visual_prompt": "月光森林湖面，10岁东亚女孩，黑色齐肩短发，黄色星星发夹，蓝色连帽外套，红色小背包，白色云朵兔，蓝色星光鲸跃出湖面，儿童绘本，柔和水彩，统一角色外观"}], "moral": "真正的勇气来自愿意和朋友一起面对未知，也来自把善意传递给需要帮助的人。", "metadata": {"request": asdict(request), "mode": "offline_demo"}}
def extract_json(text: str) -> dict[str, Any]:
    candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", candidate, flags=re.S)
        if not match:
            raise ValueError("模型输出中没有可解析JSON")
        return json.loads(match.group(0))
def validate_story(story: dict[str, Any]) -> dict[str, Any]:
    for key in ("title", "characters", "scenes", "moral"):
        if key not in story:
            raise ValueError(f"缺少字段: {key}")
    for character in story["characters"]:
        for key in ("name", "traits", "appearance"):
            if key not in character:
                raise ValueError(f"角色缺少字段: {key}")
    for scene in story["scenes"]:
        for key in ("scene_id", "description", "text", "mood", "visual_prompt"):
            if key not in scene:
                raise ValueError(f"场景缺少字段: {key}")
    return story
def generate_story(request: StoryRequest, strategy: str = "role_playing") -> dict[str, Any]:
    env = load_env(); base_url = env.get("OPENAI_BASE_URL", "").rstrip("/"); api_key = env.get("OPENAI_API_KEY", "")
    if not (base_url and api_key):
        story = demo_story(request); story["metadata"]["strategy"] = strategy; return story
    prompt = f"你是一名儿童文学作者。请返回严格JSON，不要Markdown围栏。输入：主角={request.protagonist}，主角年龄={request.protagonist_age}，兴趣={request.interest}，场景={request.setting}，主题={request.theme}，长度={request.length}，目标受众={request.audience_age}。至少3个角色、3个场景，字段严格遵循：{json.dumps(SCHEMA, ensure_ascii=False)}。Prompt策略={strategy}。"
    payload = {"model": env.get("OPENAI_MODEL", "gpt-4o-mini"), "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    request_data = urllib.request.Request(base_url + "/chat/completions", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request_data, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    story = validate_story(extract_json(data["choices"][0]["message"]["content"]))
    story.setdefault("metadata", {}).update({"strategy": strategy, "mode": "api"}); return story
if __name__ == "__main__":
    output = ROOT / "outputs" / "story_structured.json"; write_json(output, generate_story(StoryRequest())); print(output)
