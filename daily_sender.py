#!/usr/bin/env python3
"""
Everything-for-AI 定时发送脚本

为所有项目添加飞书定时发送功能：
- inspiration-bot: 每日名言
- weather-bot: 天气
- joke-bot: 笑话
- news-digest-bot: 新闻
- daily-report-generator: 日报
- weekly-summary: 周报

使用方式：
python3 daily_sender.py --type all      # 发送所有
python3 daily_sender.py --type quote    # 只发送名言
python3 daily_sender.py --type weather   # 只发送天气
"""

import sys
import subprocess
import requests
import json
from pathlib import Path
from datetime import datetime, timedelta

# 配置
REPO_DIR = Path(__file__).parent
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


def send_to_feishu(token, receiver_id, content):
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
    return resp.json().get("code") == 0


def get_inspiration():
    """获取每日名言"""
    try:
        result = subprocess.run(
            ["python3", "quote_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "inspiration-bot"),
            timeout=30
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"获取名言失败: {e}")
        return None


def get_weather():
    """获取天气"""
    try:
        result = subprocess.run(
            ["python3", "weather_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "weather-bot"),
            timeout=30
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"获取天气失败: {e}")
        return None


def get_jokes():
    """获取笑话"""
    try:
        result = subprocess.run(
            ["python3", "joke_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "joke-bot"),
            timeout=30
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"获取笑话失败: {e}")
        return None


def get_news():
    """获取新闻"""
    try:
        result = subprocess.run(
            ["python3", "news_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "news-digest-bot"),
            timeout=30
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"获取新闻失败: {e}")
        return None


def get_daily_report():
    """获取日报"""
    try:
        result = subprocess.run(
            ["python3", "daily.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "daily-report-generator"),
            timeout=60
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"获取日报失败: {e}")
        return None


def get_weekly_summary():
    """获取周报"""
    try:
        result = subprocess.run(
            ["python3", "summary.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "weekly-summary"),
            timeout=60
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"获取周报失败: {e}")
        return None


def send_all():
    """发送所有内容"""
    now = datetime.now()
    print(f"\n{'='*50}")
    print(f"📤 定时发送 - {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")

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

    results = {}

    # 1. 名言
    print("🌅 获取名言...")
    quote = get_inspiration()
    if quote:
        quote = quote.strip()
        if send_to_feishu(token, RECEIVER_ID, f"🌅 **每日名言**\n\n{quote}"):
            results["名言"] = "✅"
        else:
            results["名言"] = "❌"
    else:
        results["名言"] = "⚠️"

    # 2. 天气
    print("🌤️ 获取天气...")
    weather = get_weather()
    if weather:
        weather = weather.strip()
        if send_to_feishu(token, RECEIVER_ID, f"🌤️ **今日天气**\n\n{weather}"):
            results["天气"] = "✅"
        else:
            results["天气"] = "❌"
    else:
        results["天气"] = "⚠️"

    # 3. 笑话
    print("😄 获取笑话...")
    jokes = get_jokes()
    if jokes:
        jokes = jokes.strip()
        if send_to_feishu(token, RECEIVER_ID, f"😄 **每日一笑**\n\n{jokes}"):
            results["笑话"] = "✅"
        else:
            results["笑话"] = "❌"
    else:
        results["笑话"] = "⚠️"

    # 4. 新闻
    print("📰 获取新闻...")
    news = get_news()
    if news:
        news = news.strip()
        if send_to_feishu(token, RECEIVER_ID, f"📰 **每日新闻**\n\n{news}"):
            results["新闻"] = "✅"
        else:
            results["新闻"] = "❌"
    else:
        results["新闻"] = "⚠️"

    # 5. 日报
    print("📋 获取日报...")
    report = get_daily_report()
    if report:
        report = report.strip()
        if send_to_feishu(token, RECEIVER_ID, f"📋 **今日日报**\n\n{report}"):
            results["日报"] = "✅"
        else:
            results["日报"] = "❌"
    else:
        results["日报"] = "⚠️"

    # 6. 周报 (周一)
    if now.weekday() == 0:  # Monday
        print("📊 获取周报...")
        summary = get_weekly_summary()
        if summary:
            summary = summary.strip()
            if send_to_feishu(token, RECEIVER_ID, f"📊 **本周周报**\n\n{summary}"):
                results["周报"] = "✅"
            else:
                results["周报"] = "❌"
        else:
            results["周报"] = "⚠️"

    # 汇总
    print(f"\n{'='*50}")
    print("📊 发送结果汇总:")
    for item, status in results.items():
        print(f"   {status} {item}")
    print(f"{'='*50}\n")


def main():
    if len(sys.argv) > 1:
        send_type = sys.argv[1]
        if send_type == "--test":
            # 测试模式 - 发送一条测试消息
            config = load_config()
            app_id = config.get("channels", {}).get("feishu", {}).get("appId")
            app_secret = load_secret()
            token = get_tenant_access_token(app_id, app_secret)
            if token:
                content = f"🧪 测试消息 - {datetime.now().strftime('%H:%M')}\n\n定时发送脚本测试成功！"
                if send_to_feishu(token, RECEIVER_ID, content):
                    print("✅ 测试消息已发送！")
                else:
                    print("❌ 发送失败")
            return

    send_all()


if __name__ == "__main__":
    main()
