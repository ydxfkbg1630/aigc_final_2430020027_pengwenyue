# 视频流程说明

采用教师允许的剪辑式路线：结构化故事 → Pollinations 场景图 → Edge TTS 旁白 → SRT 字幕 → imageio-ffmpeg 合成 MP4。每幕 24 秒，三幕总片长超过 60 秒；字幕文本直接来自结构化故事的 `text` 字段，避免手工转写误差。

背景音乐位置预留在 `src/video_maker.py` 的音频输入接口，演示版本使用免费语音轨道和安静画面完成流程，现场展示时可以叠加 `outputs/audio/` 中的音色样本。视频与字幕分别为 `outputs/video/story_video.mp4` 和 `outputs/video/story.srt`。
