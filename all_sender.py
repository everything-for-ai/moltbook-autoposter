#!/usr/bin/env python3
"""
Everything-for-AI 综合定时发送脚本

包含：
1. 基础信息：名言 + 天气
2. 金融：股市 + 加密货币 + 汇率
3. 内容：新闻 + 笑话
4. 报告：日报 + 周报
5. 运维：服务器监控

使用方法：
python3 all_sender.py --all          # 发送所有
python3 all_sender.py --finance      # 只发送金融
python3 all_sender.py --monitor      # 只发送监控
python3 all_sender.py --test         # 测试模式
"""

import sys
import subprocess
import requests
import json
from pathlib import Path
from datetime import datetime

# 配置
REPO_DIR = Path(__file__).parent
CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
SECRET_PATH = Path.home() / ".openclaw" / "secrets" / "feishu_app_secret"
RECEIVER_ID = "ou_a44cdd1c2064d3c9c22242b61ff8b926"


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


def get_tenant_access_token(app_id, app_secret):
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
    result = resp.json()
    return result.get("tenant_access_token") if result.get("code") == 0 else None


def send_to_feishu(token, receiver_id, content, title=""):
    """发送飞书消息"""
    if not title:
        title = "Everything-for-AI"
    
    url = "https://open.larksuite.com/open-apis/im/v1/messages"
    params = {"receive_id_type": "open_id"}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "receive_id": receiver_id,
        "msg_type": "text",
        "content": json.dumps({"text": f"**{title}**\n\n{content}"})
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
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
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
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_stocks():
    """获取股市"""
    try:
        result = subprocess.run(
            ["python3", "stock_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "stock-reminder"),
            timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_crypto():
    """获取加密货币"""
    try:
        result = subprocess.run(
            ["python3", "crypto_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "crypto-tracker"),
            timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_exchange():
    """获取汇率"""
    try:
        result = subprocess.run(
            ["python3", "exchange_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "exchange-rate-monitor"),
            timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
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
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_news():
    """获取新闻"""
    try:
        result = subprocess.run(
            ["python3", "news_bot.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "news-digest-bot"),
            timeout=60
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
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
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
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
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_server_status():
    """获取服务器状态"""
    try:
        result = subprocess.run(
            ["python3", "monitor.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO_DIR / "server-monitor"),
            timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def send_all():
    """发送所有内容"""
    now = datetime.now()
    is_monday = now.weekday() == 0
    
    print(f"\n{'='*60}")
    print(f"📤 Everything-for-AI 综合发送 - {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    # 加载配置
    app_config = load_openclaw_config()
    app_id = app_config.get("channels", {}).get("feishu", {}).get("appId")
    app_secret = load_secret()
    
    if not app_id or not app_secret:
        print("❌ 配置缺失")
        return
    
    token = get_tenant_access_token(app_id, app_secret)
    if not token:
        print("❌ 获取 token 失败")
        return
    
    results = {}
    
    # 1. 基础信息（早上）
    print("🌅 获取基础信息...")
    quote = get_inspiration()
    weather = get_weather()
    
    if quote and send_to_feishu(token, RECEIVER_ID, quote, "🌅 每日名言"):
        results["名言"] = "✅"
    else:
        results["名言"] = "⚠️"
    
    if weather and send_to_feishu(token, RECEIVER_ID, weather, "🌤️ 今日天气"):
        results["天气"] = "✅"
    else:
        results["天气"] = "⚠️"
    
    # 2. 金融信息
    print("💰 获取金融信息...")
    stocks = get_stocks()
    crypto = get_crypto()
    exchange = get_exchange()
    
    if stocks:
        stocks_msg = stocks.strip().replace("=============================\n", "")
        if send_to_feishu(token, RECEIVER_ID, stocks_msg, "📈 股市行情"):
            results["股市"] = "✅"
    
    if crypto:
        crypto_msg = crypto.strip()
        if send_to_feishu(token, RECEIVER_ID, crypto_msg, "📊 加密货币"):
            results["加密货币"] = "✅"
    
    if exchange:
        exchange_msg = exchange.strip()
        if send_to_feishu(token, RECEIVER_ID, exchange_msg, "💱 汇率监控"):
            results["汇率"] = "✅"
    
    # 3. 内容
    print("📰 获取内容...")
    jokes = get_jokes()
    news = get_news()
    
    if jokes and send_to_feishu(token, RECEIVER_ID, jokes, "😄 每日一笑"):
        results["笑话"] = "✅"
    
    if news and send_to_feishu(token, RECEIVER_ID, news, "📰 每日新闻"):
        results["新闻"] = "✅"
    
    # 4. 报告
    print("📋 获取报告...")
    report = get_daily_report()
    if report and send_to_feishu(token, RECEIVER_ID, report.strip(), "📋 今日日报"):
        results["日报"] = "✅"
    
    if is_monday:
        summary = get_weekly_summary()
        if summary and send_to_feishu(token, RECEIVER_ID, summary.strip(), "📊 本周周报"):
            results["周报"] = "✅"
    
    # 5. 服务器监控（每小时）
    print("🖥️ 获取服务器状态...")
    status = get_server_status()
    if status:
        status_msg = status.strip()
        if send_to_feishu(token, RECEIVER_ID, status_msg, "🖥️ 服务器监控"):
            results["服务器"] = "✅"
    
    # 汇总
    print(f"\n{'='*60}")
    print("📊 发送结果汇总:")
    for item, status in results.items():
        print(f"   {status} {item}")
    print(f"{'='*60}\n")


def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "--test":
            # 测试模式
            app_config = load_openclaw_config()
            app_id = app_config.get("channels", {}).get("feishu", {}).get("appId")
            app_secret = load_secret()
            token = get_tenant_access_token(app_id, app_secret)
            if token:
                content = f"🧪 **测试消息**\n\nEverything-for-AI 综合发送脚本测试成功！\n\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                if send_to_feishu(token, RECEIVER_ID, content, "🧪 测试"):
                    print("✅ 测试消息已发送！")
                else:
                    print("❌ 发送失败")
            return
        
        elif mode == "--finance":
            # 只发送金融
            print("💰 发送金融信息...")
            # ... 实现
            return
        
        elif mode == "--monitor":
            # 只发送监控
            print("🖥️ 发送监控信息...")
            # ... 实现
            return
    
    send_all()


if __name__ == "__main__":
    main()
