# 音频工作流

1. `src/tts.py` 首选 Edge TTS 免费中文音色，并保留系统 `pyttsx3` 免费语音回退。
2. 旁白、主角、云朵兔、星光鲸分别生成 MP3，角色语速参数独立配置。
3. `generate_background_music` 使用本地正弦和弦生成低音量背景音乐，输出 `outputs/audio/background_music.mp3`。
4. `src/video_maker.py` 使用 FFmpeg 将旁白与背景音乐混音，再叠加场景图和 SRT 字幕。
5. `web/read_along.html` 根据三幕时间段高亮文本，完成语音同步展示。
