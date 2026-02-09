# Stock Reminder / 股票提醒机器人

<div class="tabs">
<details open>
<summary><span>🇨🇳 中文 (默认)</span></summary>

## 📈 股票提醒机器人

A股/ETF 实时行情监控与提醒

### 功能特点
- 📊 实时行情（腾讯财经，免费）
- ⏰ 定时推送（每天 10:00 / 16:00）
- 📝 自动涨跌分析
- ⚠️ 价格预警（涨跌 ±3%）

### 支持的股票
| 代码 | 名称 | 类型 |
|------|------|------|
| 159941 | 纳指100LOF | ETF |
| 513100 | 纳指100 | ETF (深基) |
| 600519 | 贵州茅台 | A 股 |
| 000001 | 平安银行 | A 股 |
| 513050 | 中概互联网 | ETF |

### 自选股配置

编辑 `config.json` 添加/删除自选股：

```json
{
    "schedule": ["10:00", "16:00"],
    "stocks": [
        {"code": "159941", "name": "你的名称", "type": "etf"},
        {"code": "513100", "name": "你的名称", "type": "etf"},
        {"code": "600519", "name": "贵州茅台", "type": "stock"}
    ],
    "thresholds": {"rise": 3.0, "fall": -3.0}
}
```

**字段说明：**
- `code`: 股票代码（支持 A 股、ETF）
- `name`: 自定义显示名称
- `type`: `stock` (A股) 或 `etf` (ETF)
- `thresholds`: 涨跌预警阈值（%）

### 快速开始
```bash
cd stock-reminder
pip install -r requirements.txt
python stock_bot.py
```

</details>
<details>
<summary><span>🇺🇸 English</span></summary>

## 📈 Stock Reminder

Real-time A-share/ETF monitoring with alerts

### Features
- 📊 Real-time quotes (Tencent Finance, free)
- ⏰ Scheduled push (10:00 / 16:00 daily)
- 📝 Automatic trend analysis
- ⚠️ Price alerts (> ±3%)

### Supported Stocks
| Code | Name | Type |
|------|------|------|
| 159941 | Nasdaq 100 LOF | ETF |
| 513100 | Nasdaq 100 | ETF |
| 600519 | Kweichow Moutai | A-share |

### Add Your Stocks

Edit `config.json`:

```json
{
    "schedule": ["10:00", "16:00"],
    "stocks": [
        {"code": "159941", "name": "Your Name", "type": "etf"},
        {"code": "513100", "name": "Your Name", "type": "etf"}
    ],
    "thresholds": {"rise": 3.0, "fall": -3.0}
}
```

### Quick Start
```bash
cd stock-reminder
pip install -r requirements.txt
python stock_bot.py
```

</details>
</div>

---

## 项目结构

```
stock-reminder/
├── stock_bot.py      # 主程序
├── stock_api.py      # 股票接口
├── config.json       # 配置文件（自选股）
├── stock_history.json # 历史数据（自动生成）
└── requirements.txt  # 依赖
```

## 数据来源

- 腾讯财经 (http://qt.gtimg.cn)
- 免费接口，无需 API Key

## License

MIT
