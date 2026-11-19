# 素材库构建说明

`data/templates/` 包含10个故事模板；`data/images/` 包含20张图片素材；`data/sounds/` 包含5种音效元数据；`data/characters/` 和 `data/scenes/` 提供角色、场景字段。

文本索引使用轻量向量空间和余弦相似度，可直接运行于 Python 标准环境。图像检索接口预留 `CLIPRetriever` 扩展位置，当前演示素材通过统一 `image_id` 接入，避免下载大型权重。部署到含 CLIP 权重的环境时，把图像编码器替换为 OpenCLIP，并复用相同返回字段。
