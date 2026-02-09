#!/usr/bin/env python3
"""
News Digest Bot - 每日热点汇总
阮一峰博客 + B站热门（真实数据）
"""

import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List


class NewsDigestBot:
    """热点汇总机器人"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
    
    def load_config(self, config_file: str) -> Dict:
        default_config = {
            "schedule": "09:00",
            "sources": ["ruanyifeng", "bilibili"],
            "count": 5,
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        
        return default_config
    
    def get_ruanyifeng(self) -> List[Dict]:
        """阮一峰博客 - RSS（真实数据）"""
        try:
            url = "https://www.ruanyifeng.com/blog/atom.xml"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            r = urllib.request.urlopen(req, timeout=10)
            data = r.read().decode('utf-8')
            
            root = ET.fromstring(data)
            NS = '{http://www.w3.org/2005/Atom}'
            
            news = []
            for entry in root.findall(f'{NS}entry')[:5]:
                title = entry.find(f'{NS}title')
                link = entry.find(f'{NS}link')
                summary = entry.find(f'{NS}summary')
                updated = entry.find(f'{NS}updated')
                
                news.append({
                    "title": title.text if title is not None else "No title",
                    "url": link.get('href') if link is not None else "#",
                    "source": "阮一峰博客",
                    "summary": summary.text[:80] if summary is not None else "",
                    "date": updated.text[:10] if updated is not None else ""
                })
            return news
        except Exception as e:
            print(f"阮一峰 Error: {e}")
        return []
    
    def get_bilibili(self) -> List[Dict]:
        """B站热门视频（真实 API）"""
        try:
            url = "https://api.bilibili.com/x/web-interface/popular?ps=10"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            r = urllib.request.urlopen(req, timeout=10)
            data = json.loads(r.read().decode('utf-8'))
            
            news = []
            for item in data.get('data', {}).get('list', [])[:10]:
                stat = item.get('stat', {})
                news.append({
                    "title": item.get('title', 'No title'),
                    "url": f"https://www.bilibili.com/video/av{item.get('aid', '')}",
                    "source": "B站热门",
                    "views": stat.get('view', 0),
                    "danmaku": stat.get('danmaku', 0),
                    "author": item.get('owner', {}).get('name', '')
                })
            return news
        except Exception as e:
            print(f"B站 Error: {e}")
        return []
    
    def format_message(self, news: List[Dict], source: str) -> str:
        """格式化输出"""
        if not news:
            return ""
        
        source_map = {
            "ruanyifeng": ("📖 阮一峰博客", "📅"),
            "bilibili": ("📺 B站热门", "👀")
        }
        
        title, emoji = source_map.get(source, ("📰", "•"))
        lines = [f"\n{title}\n"]
        lines.append("-" * 40)
        
        for i, item in enumerate(news[:5], 1):
            title_text = item.get('title', '无标题')[:45]
            url = item.get('url', '#')
            
            if source == "ruanyifeng":
                date = item.get('date', '')
                lines.append(f"{i}. {title_text}")
                lines.append(f"   📅 {date} | 🔗 {url}")
            else:
                views = item.get('views', 0)
                views_str = f"{views//10000}万" if views > 10000 else str(views)
                author = item.get('author', '')
                lines.append(f"{i}. {title_text}")
                lines.append(f"   {emoji} {views_str} | UP: {author}")
                lines.append(f"   🔗 {url}")
        
        return '\n'.join(lines)
    
    def run(self) -> str:
        """主程序"""
        lines = [f"📰 每日热点 - {datetime.now().strftime('%Y-%m-%d')}\n"]
        lines.append("=" * 40)
        
        for source in self.config.get("sources", []):
            if source == "ruanyifeng":
                news = self.get_ruanyifeng()
            elif source == "bilibili":
                news = self.get_bilibili()
            else:
                news = []
            lines.append(self.format_message(news, source))
        
        lines.append("\n#热点 #每日汇总")
        message = '\n'.join(lines)
        print(message)
        return message


if __name__ == "__main__":
    bot = NewsDigestBot()
    bot.run()
