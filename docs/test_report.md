# 测试报告

执行命令：

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/run_evaluation.py
py -3.12 scripts/verify_submission.py
```

测试结果由命令输出和 `outputs/reports/verification.json` 记录。质量评估维度包括 JSON 字段、媒体文件、素材数量、检索 Precision@5、Agent 事件日志、姓名一致性、ZIP CRC。
