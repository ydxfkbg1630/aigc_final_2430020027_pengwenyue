# 使用说明

1. 安装 Python 3.12 与依赖。
2. 复制 `.env.example` 为 `.env`。
3. 直接运行 `py -3.12 scripts/generate_demo.py --demo`。
4. 打开 `web/index.html`，或在项目根目录运行 `py -3.12 -m http.server 8000 --directory web`。
5. 查看 `outputs/storybook.pdf`、`outputs/video/story_video.mp4`、`web/read_along.html`。
6. 运行 `py -3.12 scripts/run_evaluation.py` 生成策略对比和检索评估。
7. 运行 `py -3.12 scripts/verify_submission.py` 生成验证报告和提交包。

## API配置

文本 API 使用 OpenAI 兼容接口，配置 `OPENAI_BASE_URL`、`OPENAI_API_KEY`、`OPENAI_MODEL`。未配置时使用离线演示模板，接口配置可直接替换为可用免费额度服务。

图像 API 直接调用 Pollinations 免费接口，生图失败时保留本地演示降级图。语音使用 Edge TTS 免费服务，生成失败时保留可识别的离线音频占位并继续完成图片和视频流程。
