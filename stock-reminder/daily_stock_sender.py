#!/usr/bin/env python3
"""
每日股市提醒定时发送脚本

使用 cron 设置定时任务：
0 14 * * * cd /root/.openclaw/workspace/everything-for-ai/stock-reminder && python3 daily_stock_sender.py

或直接运行测试：
python3 daily_stock_sender.py
"""

import sys
import subprocess
import requests
import json
from pathlib import Path

# 配置
SCRIPT_DIR = Path(__file__).parent
FEISHU_SENDER = SCRIPT_DIR / ".." / ".." / "skills" / "lark-integration" / "scripts" / "feishu-sender.py"

# 飞书配置
CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
SECRET_PATH = Path.home() / ".openclaw" / "secrets" / "feishu_app_secret"
RECEIVER_ID = "ou_a44cdd1c2064d3c9c22242b61ff8b926"


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}


def load_secret():
    if SECRET_PATH.exists():
        with open(SECRET_PATH, 'r') as f:
            return f.read().strip()
    return None


def get_tenant_access_token(app_id, app_secret):
    """获取 tenant_access_token"""
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = {"app_id": app_id, "app_secret": app_secret}
    resp = requests.post(url, json=data)
    result = resp.json()
    return result.get("tenant_access_token") if result.get("code") == 0 else None


def send_message(token, receiver_id, content):
    """发送飞书消息"""
    url = "https://open.larksuite.com/open-apis/im/v1/messages"
    params = {"receive_id_type": "open_id"}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "receive_id": receiver_id,
        "msg_type": "text",
        "content": json.dumps({"text": content})
    }
    resp = requests.post(url, params=params, headers=headers, json=data)
    result = resp.json()
    return result.get("code") == 0


def get_stock_info():
    """获取股市信息"""
    try:
        result = subprocess.run(
            ["python3", "stock_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR),
            timeout=30
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"获取股市信息失败: {e}")
        return None


def main():
    from datetime import datetime
    print(f"📊 {datetime.now().strftime('%Y-%m-%d %H:%M')} - 获取股市信息...")

    # 获取股市信息
    stock_info = get_stock_info()
    if not stock_info:
        print("❌ 获取股市信息失败")
        return

    # 发送到飞书
    config = load_config()
    app_id = config.get("channels", {}).get("feishu", {}).get("appId")
    app_secret = load_secret()

    if not app_id or not app_secret:
        print("❌ 配置缺失")
        return

    token = get_tenant_access_token(app_id, app_secret)
    if not token:
        print("❌ 获取 token 失败")
        return

    # 发送消息
    content = f"📈 **每日股市提醒** - {datetime.now().strftime('%Y-%m-%d')}\n\n{stock_info}"
    content = content.replace("=============================\n", "")
    content = content.replace("\n", "\n")

    if send_message(token, RECEIVER_ID, content):
        print("✅ 股市提醒已发送！")
    else:
        print("❌ 发送失败")


if __name__ == "__main__":
    main()
