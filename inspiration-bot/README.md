# Inspiration Bot 🌅

每日名言推送机器人

## 功能

- 每天推送励志名言
- 支持多语言（中文为主）
- 可配置定时任务

## 使用方法

```bash
cd inspiration-bot
python3 quote_bot.py
```

## 输出示例

```
🌅 每日名言 - 02/03

1. "生活不止眼前的苟且，还有诗和远方。"
   —— 高晓松

2. "你的时间有限，不要为别人而活。"
   —— 乔布斯

#名言 #励志 #每日一句
```

## 定时任务

配合 cron 使用：

```bash
# 每天早上 8 点推送
0 8 * * * cd /path/to/inspiration-bot && python3 quote_bot.py
```

## 依赖

- Python 3.x
- 无需外部 API（内置名言库）

## License

MIT
