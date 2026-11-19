from __future__ import annotations
import subprocess, wave
from pathlib import Path
from .base import ROOT

def _silent_wav(path: Path, seconds: int = 12) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as stream:
        stream.setnchannels(1); stream.setsampwidth(2); stream.setframerate(16000); stream.writeframes(b'\x00\x00' * 16000 * seconds)
    return path

def write_srt(story: dict, path: Path, seconds_per_scene: int = 24) -> Path:
    def stamp(sec: int) -> str: return f'00:00:{sec:02d},000'
    lines=[]
    for index,scene in enumerate(story['scenes'],1):
        start=(index-1)*seconds_per_scene; end=index*seconds_per_scene; lines.extend([str(index),f'{stamp(start)} --> {stamp(end)}',scene['text'],''])
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text('\n'.join(lines),encoding='utf-8'); return path

def make_slideshow(images: list[Path], audio: Path | None, output: Path, subtitle: Path | None = None, seconds_per_image: int = 24) -> Path:
    import imageio_ffmpeg
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe(); output.parent.mkdir(parents=True,exist_ok=True)
    concat=output.with_suffix('.concat.txt'); concat.write_text('\n'.join([f"file '{p.resolve().as_posix()}'\nduration {seconds_per_image}" for p in images]+[f"file '{images[-1].resolve().as_posix()}'"]),encoding='utf-8')
    duration=len(images)*seconds_per_image
    base=[ffmpeg,'-y','-f','concat','-safe','0','-i',str(concat)]
    if audio and audio.exists() and audio.stat().st_size>1000:
        command=base+['-stream_loop','-1','-i',str(audio),'-map','0:v:0','-map','1:a:0','-t',str(duration),'-vf','scale=1280:720,format=yuv420p','-r','25','-c:v','libx264','-c:a','aac','-b:a','128k',str(output)]
    else:
        command=base+['-t',str(duration),'-vf','scale=1280:720,format=yuv420p','-r','25','-an','-c:v','libx264',str(output)]
    try:
        subprocess.run(command,check=True,capture_output=True,encoding='utf-8',errors='ignore')
    except Exception:
        fallback=base+['-t',str(duration),'-vf','scale=1280:720,format=yuv420p','-r','25','-an','-c:v','libx264',str(output)]
        subprocess.run(fallback,check=True,capture_output=True,encoding='utf-8',errors='ignore')
    return output

def make_story_video(story: dict, images: list[Path], audio: Path | None = None, output_dir: Path | None = None) -> tuple[Path, Path]:
    output_dir=output_dir or ROOT/'outputs/video'; output_dir.mkdir(parents=True,exist_ok=True); subtitle=write_srt(story,output_dir/'story.srt'); return make_slideshow(images,audio,output_dir/'story_video.mp4',subtitle),subtitle
