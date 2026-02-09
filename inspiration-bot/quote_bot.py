#!/usr/bin/env python3
"""
Inspiration Bot - Daily quotes and inspiration delivery
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List


class InspirationBot:
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.quotes = self.load_quotes()
    
    def load_config(self, config_file: str) -> Dict:
        default_config = {
            "schedule": "08:00",
            "platforms": ["feishu"],
            "language": "chinese"
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        
        return default_config
    
    def load_quotes(self) -> Dict[str, List[Dict]]:
        return {
            "chinese": [
                {"text": "路漫漫其修远兮，吾将上下而求索。", "author": "屈原"},
                {"text": "天生我材必有用，千金散尽还复来。", "author": "李白"},
                {"text": "长风破浪会有时，直挂云帆济沧海。", "author": "李白"},
                {"text": "会当凌绝顶，一览众山小。", "author": "杜甫"},
                {"text": "人生得意须尽欢，莫使金樽空对月。", "author": "李白"},
                {"text": "山重水复疑无路，柳暗花明又一村。", "author": "陆游"},
                {"text": "宝剑锋从磨砺出，梅花香自苦寒来。", "author": "警世贤文"},
                {"text": "书山有路勤为径，学海无涯苦作舟。", "author": "韩愈"}
            ],
            "english": [
                {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
                {"text": "Stay hungry, stay foolish.", "author": "Steve Jobs"},
                {"text": "Your time is limited, don't waste it living someone else's life.", "author": "Steve Jobs"},
                {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
                {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
                {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
                {"text": "The best way to predict the future is to create it.", "author": "Peter Drucker"},
                {"text": "Success is not final, failure is not fatal.", "author": "Winston Churchill"}
            ],
            "tech": [
                {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
                {"text": "Programming is not about what you know; it's about what you can figure out.", "author": "Chris Pine"},
                {"text": "The only bug you can't fix is the one you don't find.", "author": "Unknown"},
                {"text": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House"},
                {"text": "Simplicity is the soul of efficiency.", "author": "Austin Freeman"}
            ]
        }
    
    def get_daily_quote(self) -> str:
        lang = self.config.get("language", "chinese")
        quotes_list = self.quotes.get(lang, self.quotes["chinese"])
        quote = random.choice(quotes_list)
        
        return f"""
🌅 每日名言

「{quote['text']}」

— {quote['author']}
        """.strip()
    
    def run(self):
        message = self.get_daily_quote()
        print(message)
        return message


if __name__ == "__main__":
    bot = InspirationBot()
    bot.run()
