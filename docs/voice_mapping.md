# 音色映射与情感方案

| 角色 | Edge TTS 音色 | 语速 | 音调 | 情感标注 | 文件 |
|---|---|---|---|---|---|
| 旁白 | zh-CN-XiaoxiaoNeural | +0% | +0Hz | 神秘、温暖 | `outputs/audio/narrator.mp3` |
| 彭文玥 | zh-CN-XiaoyiNeural | +0% | +0Hz | 好奇、坚定 | `outputs/audio/protagonist.mp3` |
| 云朵兔 | zh-CN-YunxiNeural | +0% | +0Hz | 温柔、谨慎 | `outputs/audio/rabbit.mp3` |
| 星光鲸 | zh-CN-YunyangNeural | +0% | +0Hz | 沉稳、感动 | `outputs/audio/whale.mp3` |

音频网页：`web/read_along.html`。网页按照场景时间段高亮文本，语音参数由 `src/tts.py` 统一管理。

Edge TTS 连接受限时，脚本自动切换到 Windows 中文系统音色生成 MP3；两条路径都保持角色、语速和情感字段一致。
