# 免费生图接口记录

默认演示使用本地缓存式降级图，保证离线运行和角色锚点对比；把 `.env` 中的 `USE_REMOTE_IMAGES` 改为 `1` 后，`src/image_generator.py` 会调用 Pollinations 免费接口，URL 包含固定 seed、尺寸和角色 Prompt。接口结果会写入 `outputs/images/`，请求失败时继续生成本地示例图。

- 服务：Pollinations Image API
- 默认尺寸：1024x768
- seed：由角色锚点和场景编号稳定计算
- Prompt：结构化故事的 `visual_prompt` 加角色锚点
- 输出：每个场景至少一张 PNG
