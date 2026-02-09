#!/usr/bin/env python3
"""
Stock API - A股/ETF 数据接口
使用腾讯财经接口 (免费，无需 API Key)
"""

import requests
from typing import Dict, Optional


class StockAPI:
    """腾讯财经股票接口"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_a_stock(self, code: str) -> Optional[Dict]:
        """获取 A 股数据"""
        if code.startswith('6') or code.startswith('5'):
            market = 'sh'
        else:
            market = 'sz'
        
        url = f'http://qt.gtimg.cn/q={market}{code}'
        
        try:
            r = self.session.get(url, timeout=10)
            text = r.text.strip()
            if not text.startswith('v_'):
                return None
            
            data_str = text.split('="')[1].rstrip('"')
            data = data_str.split('~')
            
            if len(data) > 33:
                current = float(data[3])
                yesterday = float(data[4])
                change = current - yesterday
                change_percent = (change / yesterday * 100) if yesterday > 0 else 0
                
                return {
                    'code': data[2],
                    'name': data[1],
                    'price': current,
                    'open': float(data[5]),
                    'high': float(data[6]),
                    'low': float(data[7]),
                    'yesterday': yesterday,
                    'change': change,
                    'change_percent': change_percent,
                    'volume': int(data[8])
                }
        except Exception as e:
            print(f"股票 API 错误: {e}")
        
        return None
    
    def format_message(self, stock: Dict) -> str:
        """格式化股票信息"""
        change = stock.get('change_percent', 0)
        emoji = "📈" if change >= 0 else "📉"
        
        return f"""{emoji} {stock['name']} ({stock['code']})
💰 当前: {stock['price']:.2f}
📊 涨跌: {change:+.2f}%
📈 开盘: {stock.get('open', stock['price']):.2f}
📉 最高: {stock.get('high', stock['price']):.2f}
⬆️ 最低: {stock.get('low', stock['price']):.2f}
📊 成交量: {stock.get('volume', 0):,} 手"""


# 测试
if __name__ == "__main__":
    api = StockAPI()
    
    stocks = ["600519", "000001", "513100", "513050"]
    for code in stocks:
        stock = api.get_a_stock(code)
        if stock:
            print(api.format_message(stock))
            print()
