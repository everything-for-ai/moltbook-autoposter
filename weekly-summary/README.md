# Weekly Summary 📊

每周总结报告生成器

## 功能

- 自动生成每周工作报告
- 汇总已完成任务
- 统计工作时长
- 支持多种格式输出

## 使用方法

```bash
cd weekly-summary
python3 summary.py
```

## 输出示例

```
📊 周报 - 第 5 周 (2026.01.27 - 2026.02.02)

✅ 本周完成
- 项目 A 第一阶段
- Bug 修复 12 个
- 代码审查 5 次

📈 数据统计
- 提交代码: 23 次
- 代码审查: 5 次
- 文档更新: 8 篇

🎯 下周计划
- 项目 A 第二阶段
- 性能优化

#周报 #工作总结 #每周总结
```

## 配置

在 `config.json` 中配置：

```json
{
  "week_start": "monday",
  "output_format": "markdown",
  "include_metrics": true
}
```

## 定时任务

每周五下午生成：

```bash
# 每周五 17 点生成周报
0 17 * * 5 cd /path/to/weekly-summary && python3 summary.py
```

## 依赖

- Python 3.x
- 无需外部 API

## License

MIT
