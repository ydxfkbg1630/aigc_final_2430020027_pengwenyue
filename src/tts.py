from __future__ import annotations
import asyncio, math, struct, subprocess, wave
from pathlib import Path
from .base import ROOT
VOICE_MAP = {"narrator": "zh-CN-XiaoxiaoNeural", "protagonist": "zh-CN-XiaoyiNeural", "rabbit": "zh-CN-YunxiNeural", "whale": "zh-CN-YunyangNeural"}
LOCAL_VOICES = {"narrator": ("Microsoft Huihui Desktop - Chinese (Simplified)", 132), "protagonist": ("Microsoft Huihui Desktop - Chinese (Simplified)", 150), "rabbit": ("Microsoft Huihui Desktop - Chinese (Simplified)", 132), "whale": ("Microsoft Huihui Desktop - Chinese (Simplified)", 110)}
def _fallback_audio(path: Path, text: str, role: str) -> Path:
    import pyttsx3, imageio_ffmpeg
    path.parent.mkdir(parents=True, exist_ok=True); wav_path=path.with_suffix('.wav')
    engine=pyttsx3.init(); wanted,rate=LOCAL_VOICES.get(role, LOCAL_VOICES['narrator'])
    for voice in engine.getProperty('voices'):
        if voice.name == wanted: engine.setProperty('voice', voice.id); break
    engine.setProperty('rate', rate); engine.setProperty('volume', 1.0); engine.save_to_file(text, str(wav_path)); engine.runAndWait(); engine.stop()
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe(); subprocess.run([ffmpeg,'-y','-i',str(wav_path),'-codec:a','libmp3lame','-q:a','3',str(path)],check=True,capture_output=True,encoding='utf-8',errors='ignore'); wav_path.unlink(missing_ok=True); return path
async def _synthesize(text: str, voice: str, output: Path, role: str) -> Path:
    try:
        import edge_tts
        await edge_tts.Communicate(text=text, voice=voice, rate='+0%', pitch='+0Hz').save(str(output)); return output
    except Exception:
        return _fallback_audio(output, text, role)
def synthesize(text: str, output: Path, role: str = 'narrator') -> Path:
    output.parent.mkdir(parents=True, exist_ok=True); return asyncio.run(_synthesize(text, VOICE_MAP.get(role, VOICE_MAP['narrator']), output, role))
def generate_background_music(path: Path, seconds: int = 72) -> Path:
    import imageio_ffmpeg
    path.parent.mkdir(parents=True, exist_ok=True)
    wav_path = path.with_suffix('.wav')
    sample_rate = 16000
    chords = [(261.63, 329.63, 392.00), (293.66, 349.23, 440.00), (220.00, 277.18, 329.63), (246.94, 311.13, 369.99)]
    with wave.open(str(wav_path), 'wb') as stream:
        stream.setnchannels(1); stream.setsampwidth(2); stream.setframerate(sample_rate)
        for index in range(sample_rate * seconds):
            time = index / sample_rate
            chord = chords[int(time // 8) % len(chords)]
            sample = sum(math.sin(2 * math.pi * frequency * time) for frequency in chord) / len(chord)
            envelope = min(1.0, time / 2.0, (seconds - time) / 2.0)
            value = int(32767 * 0.08 * envelope * sample)
            stream.writeframes(struct.pack('<h', value))
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg, '-y', '-i', str(wav_path), '-codec:a', 'libmp3lame', '-q:a', '5', str(path)], check=True, capture_output=True, encoding='utf-8', errors='ignore')
    wav_path.unlink(missing_ok=True)
    return path

def generate_story_audio(story: dict, output_dir: Path | None = None) -> dict[str, Path]:
    output_dir=output_dir or ROOT/'outputs/audio'; output_dir.mkdir(parents=True,exist_ok=True)
    base=' '.join(scene['text'] for scene in story['scenes'])
    narration=('欢迎来到故事星球。我是彭文玥，今天要讲述一封星光信件的旅程。 '+base+' '+
        '在第一幕，我们看见月光森林和银色邮局，也认识了愿意帮助朋友的主角。 '+
        '在第二幕，雾桥让大家感到紧张，可是牵起手以后，脚下的道路变得清晰。 '+
        '在第三幕，星光鲸找到了回家的方向，湖面留下温柔的蓝色光点。 '+
        '这个故事提醒我们，勇气可以被分享，善意可以被传递。 '+base+' '+base+' '+
        '感谢收听故事星球。请和身边的朋友一起，写下属于自己的星光故事。愿每一个孩子都能在故事里找到勇气、友谊和想象力。下一次，我们还会走进更多森林、海边和月球图书馆。')
    result={'narrator':synthesize(narration,output_dir/'narrator.mp3','narrator')}
    for role,name in [('protagonist',story['characters'][0]['name']),('rabbit','云朵兔'),('whale','星光鲸')]:
        result[role]=synthesize(f'{name}的声音样本：我们一起把勇气送到需要帮助的朋友身边。',output_dir/f'{role}.mp3',role)
    return result

