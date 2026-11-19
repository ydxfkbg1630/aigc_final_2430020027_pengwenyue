# 需求实现矩阵

作者：彭文玥｜学号：2430020027｜范围：前八周作业0-6与第8周综合展示

| 需求 | 实现 | 证据 | 验证方式 |
|---|---|---|---|
| 作业0三主题交互网页 | `web/index.html` | 主题按钮、输入字段 | 浏览器打开后切换三主题 |
| 作业1六项输入 | `src/story_generator.py` | `StoryRequest` | 运行生成脚本检查字段 |
| 作业1标准JSON | `validate_story` | `outputs/story_structured.json` | `scripts/verify_submission.py` |
| 三种Prompt策略 | zero_shot/few_shot/role_playing | `docs/prompt_strategy_comparison.csv` | `scripts/run_evaluation.py` |
| 作业2免费生图 | Pollinations + fixed seed | `src/image_generator.py` | `outputs/images/` |
| 角色一致性 | 外貌锚点+稳定seed | `docs/character_consistency.md` | 场景图并排对比 |
| 作业3免费语音 | Edge TTS四音色映射 | `src/tts.py`、`docs/voice_mapping.md` | MP3文件与网页 |
| 作业4视频 | imageio-ffmpeg剪辑路线 | `src/video_maker.py`、`outputs/video/` | MP4和SRT |
| 作业5素材库 | 10模板、20图、5音效、文本检索 | `data/`、`src/rag_store.py` | `docs/retrieval_evaluation.csv` |
| 作业6 Agent | 五步计划、四类工具、两案例、干预 | `src/agent.py`、`outputs/agent_runs/` | 流程日志和架构图 |
| 综合展示 | 文本+图像+音频+视频 | `docs/final_presentation.md` | 现场运行脚本 |
| 身份信息 | 姓名统一为彭文玥 | 全仓库文本扫描 | 验证报告 `name_leaks=[]` |
