from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from .base import ROOT, write_json
from .story_generator import StoryRequest, generate_story
from .image_generator import generate_story_images
from .tts import generate_story_audio
from .video_maker import make_story_video
from .rag_store import StoryMaterialStore

@dataclass
class AgentContext:
    idea: str
    user_changes: list[str] = field(default_factory=list)
    log: list[dict] = field(default_factory=list)
    story: dict | None = None
    images: list[Path] = field(default_factory=list)
    audio: dict = field(default_factory=dict)
    video: Path | None = None

def plan(idea: str, changes: list[str] | None = None) -> list[str]:
    steps=["retrieve_materials", "write_structured_story", "generate_images", "synthesize_audio", "make_video"]
    if changes: steps.insert(1, "apply_user_intervention")
    return steps

def run_agent(idea: str, changes: list[str] | None = None) -> AgentContext:
    context=AgentContext(idea, changes or [])
    context.log.append({"event":"plan", "steps":plan(idea, changes)})
    store=StoryMaterialStore(); recommendation=store.recommend(idea); context.log.append({"event":"retrieve_materials", "recommendation":recommendation})
    protagonist="彭文玥"; theme="勇气与友谊"; setting="月光森林"
    if changes:
        for change in changes:
            context.log.append({"event":"user_intervention", "instruction":change})
            if "女孩" in change: protagonist="彭文玥"
            if "海边" in change: setting="星光海边"
    context.story=generate_story(StoryRequest(protagonist=protagonist, setting=setting, theme=theme), "agent_planning")
    context.log.append({"event":"write_structured_story", "title":context.story["title"]})
    context.images=generate_story_images(context.story); context.log.append({"event":"generate_images", "count":len(context.images)})
    context.audio=generate_story_audio(context.story); context.log.append({"event":"synthesize_audio", "roles":list(context.audio)})
    context.video,_=make_story_video(context.story, context.images, context.audio.get("narrator")); context.log.append({"event":"make_video", "path":str(context.video)})
    return context

def save_agent_run(context: AgentContext, name: str="agent_run") -> Path:
    target=ROOT/"outputs"/"agent_runs"; target.mkdir(parents=True, exist_ok=True)
    path=target/f"{name}.json"; write_json(path, {"idea":context.idea,"user_changes":context.user_changes,"log":context.log,"story":context.story,"images":[str(x) for x in context.images],"audio":{k:str(v) for k,v in context.audio.items()},"video":str(context.video) if context.video else None}); return path
