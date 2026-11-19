# AIGC多模态儿童故事工坊

作者：彭文玥  学号：2430020027

GitHub： https://github.com/ydxfkbg1630/aigc_final_2430020027_pengwenyue

本项目覆盖《AIGC应用开发实践》前八周作业 0-6 与第 8 周综合展示，主题为“故事星球：多模态儿童故事工坊”。系统把结构化故事、免费文生图、免费语音、字幕视频、素材库检索和 Agent 工作流串成一条可运行流水线。

## 快速运行

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3.12 -m pip install -r requirements.txt
Copy-Item .env.example .env
py -3.12 scripts\generate_demo.py --demo
py -3.12 scripts\run_evaluation.py
py -3.12 scripts\verify_submission.py
py -3.12 -m http.server 8000 --directory web
```

打开 `http://localhost:8000` 查看作业 0 的交互故事页。运行生成脚本后，`outputs/` 中会出现故事 JSON、配图、音频、字幕、绘本 PDF 与 MP4 示例。

## 免费服务方案

- 文本：默认离线模板；配置 `OPENAI_BASE_URL` 与 `OPENAI_API_KEY` 后可接入任意 OpenAI 兼容免费额度接口。
- 生图：`https://image.pollinations.ai` 免费接口，固定 seed 和角色外貌描述实现一致性方案一。
- 语音：Microsoft Edge TTS 免费服务，通过 `edge-tts` 生成中文普通话音频。
- 视频：本地 `imageio-ffmpeg` 合成，无需付费视频生成接口。

所有接口都设置缓存、重试和离线降级，示例运行不依赖密钥。

## 项目结构

- `web/`：作业 0 交互网页
- `src/`：故事生成、配图、语音、视频、RAG 检索、Agent 工具
- `data/`：故事模板、角色、场景、图片素材、音效索引
- `outputs/`：演示成品与评估结果
- `docs/`：每周报告、流程说明、架构图、答辩材料、AI 协作日志
- `scripts/`：一键生成、评估、验证

## 作业对应关系

| 作业 | 交付位置 |
|---|---|
| 作业0 | `web/index.html`、`docs/week1_demo_script.md` |
| 作业1 | `src/story_generator.py`、`outputs/story_structured.json`、`docs/prompt_strategy_comparison.csv` |
| 作业2 | `src/image_generator.py`、`outputs/images/`、`outputs/storybook.pdf`、`docs/character_consistency.md` |
| 作业3 | `src/tts.py`、`outputs/audio/`、`docs/audio_workflow.md` |
| 作业4 | `src/video_maker.py`、`outputs/video/`、`docs/video_workflow.md` |
| 作业5 | `src/rag_store.py`、`outputs/retrieval/`、`docs/retrieval_evaluation.csv` |
| 作业6 | `src/agent.py`、`outputs/agent_runs/`、`docs/agent_architecture.svg` |
| 综合展示 | `docs/final_presentation.md`、`outputs/video/final_demo.mp4`、`docs/defense_qa.md` |

## 可复现说明

运行 `py -3.12 scripts\verify_submission.py` 会检查目录、关键字段、素材数量、ZIP CRC、敏感配置和媒体文件。免费服务产生的真实网络结果写入缓存，离线运行会保留同结构的演示结果。
