# 部署指南

## 本地部署

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 scripts/generate_demo.py --demo
py -3.12 -m http.server 8000 --directory web
```

## 配置

把免费文本 API 写入 `.env`，密钥通过环境变量注入。Pollinations 和 Edge TTS 由代码直接访问，生成结果保存在 `outputs/`。

## 验证

浏览器打开 `http://localhost:8000`；检查 `outputs/storybook.pdf`、`outputs/video/story_video.mp4` 和 `web/read_along.html`；最后运行验证脚本生成提交包。

## 常见处理

网络延迟时重复执行生成命令，已有本地输出可直接用于演示；浏览器直接打开网页时使用本地 HTTP 服务以便读取输出媒体。
