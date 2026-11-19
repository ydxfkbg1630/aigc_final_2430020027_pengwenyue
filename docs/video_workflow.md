# 视频流程说明

采用教师允许的剪辑式路线：结构化故事 → Pollinations 场景图 → 免费中文语音 → 本地背景音乐 → SRT 字幕 → imageio-ffmpeg 合成 MP4。每幕 24 秒，三幕总片长 72 秒；字幕文本直接来自结构化故事的 `text` 字段。

背景音乐由 `src/tts.py` 生成低音量和弦轨道，`src/video_maker.py` 通过 FFmpeg 与旁白混音。视频与字幕分别为 `outputs/video/story_video.mp4` 和 `outputs/video/story.srt`，旁白与背景音乐分别保存在 `outputs/audio/`。
