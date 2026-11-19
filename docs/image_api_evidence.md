# 免费生图接口记录

本次最终成品的三幕配图已通过 Pollinations Image API 实际请求生成，返回 JPEG 后统一转换为 PNG，文件保存在 `outputs/images/scene_01.png` 至 `scene_03.png`。三张图均带有 Pollinations 返回水印，便于核验接口来源。

- 服务：Pollinations Image API
- 请求地址：`https://image.pollinations.ai/prompt/<encoded-prompt>`
- 尺寸参数：1024x768
- 固定 seed：243002027、243002028、243002029
- Prompt：英文儿童绘本场景描述，包含女孩、白色兔子、月光森林、雾桥和星光湖
- 输出：三张真实 API 返回图，经 Pillow 转 PNG 后用于 PDF 与 MP4
- 代码入口：`src/image_generator.py`
- 开关：`.env` 中 `USE_REMOTE_IMAGES=1`

Pollinations 免费额度按 IP 设置时间窗口；代码保留重试和本地降级路径，课程现场可切换网络后重新生成。