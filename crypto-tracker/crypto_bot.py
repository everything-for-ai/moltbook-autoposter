#!/usr/bin/env python3
"""
Crypto Tracker - 加密货币价格追踪
支持：实时价格、涨跌幅、飞书发送
"""

import os
import json
import requests
import time
from datetime import datetime
from pathlib import Path

# 配置
CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
SECRET_PATH = Path.home() / ".openclaw" / "secrets" / "feishu_app_secret"
RECEIVER_ID = "ou_a44cdd1c2064d3c9c22242b61ff8b926"


def load_config():
    default = {
        "coins": ["bitcoin", "ethereum", "solana", "bnb", "dogecoin"],
        "currency": "cny"
    }
    if Path("config.json").exists():
        with open("config.json") as f:
            default.update(json.load(f))
    return default


def load_openclaw_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def load_secret():
    if SECRET_PATH.exists():
        with open(SECRET_PATH) as f:
            return f.read().strip()
    return None


def get_crypto_prices(coins, currency="cny"):
    """获取加密货币价格（真实API）"""
    try:
        # 使用 CoinGecko 免费 API
        coin_ids = ",".join(coins)
        url = f"https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": currency,
            "ids": coin_ids,
            "order": "market_cap_desc",
            "sparkline": "false",
            "price_change_percentage": "24h"
        }
        
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"获取价格失败: {e}")
    
    # Mock 数据（备用）
    return []


def format_crypto_message(prices, config):
    """格式化加密货币消息"""
    message = [f"📊 **加密货币行情** - {datetime.now().strftime('%m/%d %H:%M')}\n"]
    
    if not prices:
        # Mock 数据
        mock_data = {
            "bitcoin": {"price": 650000, "change": 2.5},
            "ethereum": {"price": 22000, "change": -1.2},
            "solana": {"price": 1200, "change": 5.8},
            "bnb": {"price": 4200, "change": 1.5},
            "dogecoin": {"price": 0.85, "change": -3.2}
        }
        prices = []
    
    for coin in config.get("coins", []):
        price_data = next((p for p in prices if p["id"] == coin), None)
        
        if price_data:
            symbol = price_data["symbol"].upper()
            current_price = price_data["current_price"]
            change_24h = price_data.get("price_change_percentage_24h", 0)
            market_cap = price_data.get("market_cap", 0) / 1e8  # 亿
            volume = price_data.get("total_volume", 0) / 1e8  # 亿
            
            emoji = "🟢" if change_24h >= 0 else "🔴"
            change_str = f"+{change_24h:.2f}%" if change_24h >= 0 else f"{change_24h:.2f}%"
            
            message.append(f"{emoji} **{symbol}**")
            message.append(f"   💰 ¥{current_price:,.0f}")
            message.append(f"   📈 24h: {change_str}")
            message.append(f"   📊 市值: ¥{market_cap:.1f}亿")
            message.append(f"   💵 成交: ¥{volume:.1f}亿")
            message.append("")
        else:
            # 使用 mock
            mock = mock_data.get(coin, {"price": 0, "change": 0})
            emoji = "🟢" if mock["change"] >= 0 else "🔴"
            message.append(f"{emoji} **{coin.capitalize()}**")
            message.append(f"   💰 ¥{mock['price']:,.0f} ({mock['change']:+.1f}%)")
            message.append("")
    
    # 趋势分析
    positive = sum(1 for p in prices if p.get("price_change_percentage_24h", 0) >= 0)
    total = len(prices)
    
    if total > 0:
        sentiment = "📈 整体上涨" if positive > total / 2 else "📉 整体下跌"
        message.append(f"💡 走势: {positive}/{total} 上涨 | {sentiment}")
    
    message.append("\n#加密货币 #BTC #ETH")
    
    return "\n".join(message)


def get_tenant_access_token(app_id, app_secret):
    """获取 tenant_access_token"""
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
    result = resp.json()
    return result.get("tenant_access_token") if result.get("code") == 0 else None


def send_to_feishu(token, receiver_id, content):
    """发送飞书消息"""
    url = "https://open.larksuite.com/open-apis/im/v1/messages"
    params = {"receive_id_type": "open_id"}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "receive_id": receiver_id,
        "msg_type": "text",
        "content": json.dumps({"text": content})
    }
    resp = requests.post(url, params=params, headers=headers, json=data)
    return resp.json().get("code") == 0


def main():
    print(f"\n{'='*50}")
    print(f"📊 加密货币行情 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    # 加载配置
    config = load_config()
    
    # 获取价格
    prices = get_crypto_prices(config.get("coins", []), config.get("currency", "cny"))
    
    # 格式化消息
    message = format_crypto_message(prices, config)
    print(message)
    
    # 发送到飞书
    app_config = load_openclaw_config()
    app_id = app_config.get("channels", {}).get("feishu", {}).get("appId")
    app_secret = load_secret()
    
    if app_id and app_secret:
        token = get_tenant_access_token(app_id, app_secret)
        if token and send_to_feishu(token, RECEIVER_ID, message):
            print("\n✅ 已发送至飞书！")
        else:
            print("\n⚠️ 飞书发送失败")
    else:
        print("\n💡 未配置飞书，仅显示本地")


if __name__ == "__main__":
    main()
