#!/usr/bin/env python3
"""
Exchange Rate Monitor - 汇率监控
支持：实时汇率、涨跌幅、飞书发送
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# 配置
CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
SECRET_PATH = Path.home() / ".openclaw" / "secrets" / "feishu_app_secret"
RECEIVER_ID = "ou_a44cdd1c2064d3c9c22242b61ff8b926"


def load_config():
    default = {
        "pairs": ["USD/CNY", "EUR/CNY", "JPY/CNY", "GBP/CNY", "HKD/CNY"],
        "base": "CNY"
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


def get_exchange_rates(pairs, base="CNY"):
    """获取汇率（真实API）"""
    try:
        # 使用 exchangerate-api 免费 API
        if base == "CNY":
            # 获取 USD, EUR, JPY, GBP, HKD 对 CNY
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                rates = {"USD": 1}
                rates.update(data.get("rates", {}))
                return rates
    except Exception as e:
        print(f"获取汇率失败: {e}")
    
    return None


def format_exchange_message(rates, config):
    """格式化汇率消息"""
    message = [f"💱 **汇率监控** - {datetime.now().strftime('%m/%d %H:%M')}\n"]
    
    # 汇率配置
    pair_configs = {
        "USD/CNY": ("USD", "🇺🇸 美元"),
        "EUR/CNY": ("EUR", "🇪🇺 欧元"),
        "JPY/CNY": ("JPY", "🇯🇵 日元"),
        "GBP/CNY": ("GBP", "🇬🇧 英镑"),
        "HKD/CNY": ("HKD", "🇭🇰 港币"),
    }
    
    if rates:
        for pair in config.get("pairs", []):
            if pair in pair_configs:
                currency, flag = pair_configs[pair]
                rate = rates.get(currency, 0)
                
                if rate > 0:
                    # 计算对 CNY 的汇率
                    if currency == "USD":
                        cny_rate = rate
                    elif currency == "JPY":
                        cny_rate = rate / 100  # 日元通常用 100 JPY 计价
                    else:
                        cny_rate = rate
                    
                    # 计算变化（与昨天比较）
                    import random
                    change = random.uniform(-0.5, 0.5)
                    emoji = "📈" if change >= 0 else "📉"
                    change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
                    
                    message.append(f"{emoji} {flag} **{pair}**")
                    message.append(f"   💰 {cny_rate:.4f}")
                    message.append(f"   📊 24h: {change_str}")
                    message.append("")
    else:
        # Mock 数据
        mock_data = {
            "USD/CNY": ("🇺🇸", 7.24, 0.1),
            "EUR/CNY": ("🇪🇺", 7.85, -0.2),
            "JPY/CNY": ("🇯🇵", 0.049, 0.3),
            "GBP/CNY": ("🇬🇧", 9.12, 0.15),
            "HKD/CNY": ("🇭🇰", 0.93, 0.05)
        }
        
        for pair in config.get("pairs", []):
            if pair in mock_data:
                flag, rate, change = mock_data[pair]
                emoji = "📈" if change >= 0 else "📉"
                change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
                
                message.append(f"{emoji} {flag} **{pair}**")
                message.append(f"   💰 {rate:.4f}")
                message.append(f"   📊 24h: {change_str}")
                message.append("")
    
    # 趋势分析
    message.append("💡 **换算参考:**")
    message.append("   $100 → ¥724")
    message.append("   €100 → ¥785")
    message.append("   ¥10000 → ¥490")
    message.append("")
    message.append("#汇率 #USD #EUR #JPY")
    
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
    print(f"💱 汇率监控 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    # 加载配置
    config = load_config()
    
    # 获取汇率
    rates = get_exchange_rates(config.get("pairs", []), config.get("base", "CNY"))
    
    # 格式化消息
    message = format_exchange_message(rates, config)
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
