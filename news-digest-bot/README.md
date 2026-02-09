# News Digest Bot / 每日热点汇总

<div class="tabs">
<details open>
<summary><span>🇨🇳 中文 (默认)</span></summary>

## 📰 每日热点汇总

阮一峰博客 + B站热门（真实数据获取）

### 功能特点
- ✅ **真实数据** - 只使用真实 API/RSS
- 📖 **阮一峰博客** - 技术周刊 RSS
- 📺 **B站热门** - 官方 API
- 🚫 **无模拟数据** - 不编造任何内容

### 新闻源

| 来源 | 链接 | 状态 |
|------|------|------|
| 阮一峰博客 | ruanyifeng.com/blog/atom.xml | ✅ 实时 RSS |
| B站热门 | api.bilibili.com | ✅ 实时 API |

### 配置

编辑 `config.json`：

```json
{
    "schedule": "09:00",
    "sources": ["ruanyifeng", "bilibili"],
    "count": 5
}
```

### 快速开始
```bash
cd news-digest-bot
python news_bot.py
```

</details>
<details>
<summary><span>🇺🇸 English</span></summary>

## 📰 Daily Hot Topics

Ruan Yifeng Blog + Bilibili (Real Data Only)

### Features
- ✅ **Real Data Only** - No fake content
- 📖 Ruan Yifeng Blog - Tech RSS
- 📺 Bilibili Trending - Official API
- 🚫 **No Mock Data**

### Sources

| Source | Link | Status |
|--------|------|--------|
| Ruan Yifeng | ruanyifeng.com/blog/atom.xml | ✅ RSS |
| Bilibili | api.bilibili.com | ✅ API |

### Quick Start
```bash
cd news-digest-bot
python news_bot.py
```

</details>
</div>

---

## 当前数据（真实）

**阮一峰博客：**
- 科技爱好者周刊（第 383 期）：你是第几级 AI 编程 (2026-02-01)
- Kimi 的一体化，Manus 的分层 (2026-01-30)

**B站热门：**
- 《原神》角色预告 (69万播放)
- 崩坏星穹铁道 (548万播放)

---

*只获取真实数据，不编造任何内容*
