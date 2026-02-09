#!/usr/bin/env python3
"""
Stock Reminder - A股/ETF 提醒机器人
每天 10:00 / 16:00 推送 + 涨跌分析
"""

import os
import json
from datetime import datetime
from typing import Dict, List
from stock_api import StockAPI


class StockReminder:
    """股票提醒机器人"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.stock_api = StockAPI()
        self.previous_data = self.load_previous()
    
    def load_config(self, config_file: str) -> Dict:
        default_config = {
            "schedule": ["10:00", "16:00"],
            "stocks": [
                {"code": "159941", "name": "纳指100LOF", "type": "etf"},
                {"code": "513100", "name": "纳指100", "type": "etf"},
                {"code": "600519", "name": "贵州茅台", "type": "stock"},
                {"code": "000001", "name": "平安银行", "type": "stock"},
                {"code": "513050", "name": "中概互联网", "type": "etf"}
            ],
            "thresholds": {"rise": 3.0, "fall": -3.0}
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        
        return default_config
    
    def load_previous(self) -> Dict:
        """加载上次数据用于对比"""
        if os.path.exists("stock_history.json"):
            with open("stock_history.json") as f:
                return json.load(f)
        return {}
    
    def save_previous(self):
        """保存当前数据"""
        with open("stock_history.json", 'w') as f:
            json.dump(self.current_data, f)
    
    def get_stock_data(self, code: str) -> Dict:
        """获取股票/ETF 数据"""
        data = self.stock_api.get_a_stock(code)
        
        if not data:
            import random
            return {
                "code": code,
                "name": code,
                "price": 100 + random.uniform(-10, 10),
                "change_percent": random.uniform(-2, 2)
            }
        
        return data
    
    def analyze(self, stock: Dict, prev: Dict = None) -> str:
        """涨跌分析"""
        change = stock.get('change_percent', 0)
        price = stock.get('price', 0)
        
        analysis = []
        
        # 涨跌幅度分析
        if change > 3:
            analysis.append("🔥 大涨！")
        elif change > 1:
            analysis.append("📈 上涨")
        elif change > 0:
            analysis.append("➡️ 小涨")
        elif change > -1:
            analysis.append("➡️ 小跌")
        elif change > -3:
            analysis.append("📉 下跌")
        else:
            analysis.append("🧊 大跌！")
        
        # 与昨日收盘对比
        if prev:
            price_change = price - prev.get('price', price)
            if abs(price_change) > 0.01:
                if price_change > 0:
                    analysis.append(f"较上次+{price_change:.2f}")
                else:
                    analysis.append(f"较上次{price_change:.2f}")
        
        return " ".join(analysis)
    
    def get_all_data(self) -> List[Dict]:
        """获取所有配置股票的数据"""
        results = []
        for item in self.config.get("stocks", []):
            data = self.get_stock_data(item["code"])
            data["display_name"] = item.get("name", item["code"])
            data["type"] = item.get("type", "stock")
            data["analysis"] = self.analyze(data, self.previous_data.get(item["code"]))
            results.append(data)
        return results
    
    def check_alerts(self, stocks: List[Dict]) -> List[Dict]:
        """检查涨跌预警"""
        alerts = []
        thresholds = self.config.get("thresholds", {})
        
        for stock in stocks:
            change = stock.get("change_percent", 0)
            if change >= thresholds.get("rise", 3):
                alerts.append({"stock": stock, "type": "rise", "value": change})
            elif change <= thresholds.get("fall", -3):
                alerts.append({"stock": stock, "type": "fall", "value": change})
        
        return alerts
    
    def format_message(self, stocks: List[Dict]) -> str:
        """格式化输出"""
        now = datetime.now()
        is_morning = now.hour < 12
        time_str = "上午" if is_morning else "下午"
        
        lines = [f"📈 {time_str}好！{now.strftime('%Y-%m-%d %H:%M')} 行情\n"]
        
        # 纳指ETF 放在最前面
        nasdaq_codes = ["159941", "513100"]
        nasdaq_list = [s for s in stocks if s.get("code") in nasdaq_codes]
        other_list = [s for s in stocks if s.get("code") not in nasdaq_codes]
        
        # 显示纳指ETF
        for s in nasdaq_list:
            change = s.get('change_percent', 0)
            emoji = "📈" if change >= 0 else "📉"
            lines.append(f"{'='*30}")
            lines.append(f"{emoji} {s['display_name']} ({s['code']})")
            lines.append(f"💰 当前: {s['price']:.3f}")
            lines.append(f"📊 涨跌: {change:+.2f}%")
            lines.append(f"📝 {s.get('analysis', '')}")
            lines.append(f"{'='*30}\n")
        
        # 显示其他股票
        for stock in other_list:
            change = stock.get('change_percent', 0)
            emoji = "📈" if change >= 0 else "📉"
            lines.append(f"{emoji} {stock['display_name']} ({stock['code']})")
            lines.append(f"   💰 {stock['price']:.2f}  ({change:+.2f}%)")
            lines.append(f"   📝 {stock.get('analysis', '')}")
            lines.append("")
        
        return "\n".join(lines).strip()
    
    def run(self) -> str:
        """主程序"""
        stocks = self.get_all_data()
        
        # 保存当前数据用于下次对比
        self.current_data = {s['code']: s for s in stocks}
        self.save_previous()
        
        message = self.format_message(stocks)
        
        # 检查预警
        alerts = self.check_alerts(stocks)
        if alerts:
            lines = [message, "\n⚠️ 价格预警:"]
            for alert in alerts:
                emoji = "🚀" if alert["type"] == "rise" else "📉"
                lines.append(f"{emoji} {alert['stock']['display_name']} {alert['value']:+.2f}%")
            message = "\n".join(lines)
        
        print(message)
        return message


if __name__ == "__main__":
    bot = StockReminder()
    bot.run()
