# 检索评估

运行 `py -3.12 scripts/run_evaluation.py` 生成 `retrieval_evaluation.csv`。评估使用三个自然语言查询：森林里的勇气冒险、海边灯塔合作、月球图书馆阅读。每个查询返回 Top-5，统计结果相关数和 Precision@5，同时保留人工观察列。

结构化推荐字段：`template_ids`、`character_candidates`、`scene_candidates`、`image_ids`、`sound_ids`、`generation_hints`。接口由 `src/rag_store.py` 提供。
