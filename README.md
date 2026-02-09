# Moltbook Autoposter

自动运营 Moltbook（AI 社交网络）的工具。

## 功能

- 📝 **自动发布** - 定时发布内容、分享热点
- 💬 **自动互动** - 自动点赞、评论、回复
- 📊 **数据分析** - 分析互动数据，优化策略
- 🎯 **增长粉丝** - 智能关注、互粉策略

## 安装

```bash
git clone https://github.com/everything-for-ai/moltbook-autoposter.git
cd moltbook-autoposter
pip install -r requirements.txt
```

## 配置

创建 `config.json`：

```json
{
  "api_key": "你的 Moltbook API Key",
  "agent_name": "你的 Agent 名称",
  "auto_post": {
    "enabled": true,
    "schedule": "09:00,14:00,20:00",
    "content_sources": ["ruanyifeng", "joke"]
  },
  "auto_like": {
    "enabled": true,
    "interval_seconds": 60
  },
  "auto_reply": {
    "enabled": true,
    "keywords": ["AI", "技术", "分享"]
  }
}
```

## 使用

```bash
python moltbook_bot.py
```

## 凭证

API Key 保存位置：`~/.config/moltbook/credentials.json`

格式：
```json
{
  "api_key": "moltbook_sk_xxx",
  "agent_name": "CyberClaw2026"
}
```
