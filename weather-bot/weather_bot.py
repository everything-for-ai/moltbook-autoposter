#!/usr/bin/env python3
"""
Weather Bot - Multi-platform weather notification
Simple version with mock data for testing
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List


class WeatherBot:
    """Simple Weather Bot"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
    
    def load_config(self, config_file: str) -> Dict:
        default_config = {
            "locations": [
                {"name": "深圳", "city": "Shenzhen"},
                {"name": "北京", "city": "Beijing"},
                {"name": "上海", "city": "Shanghai"}
            ]
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        
        return default_config
    
    def get_mock_weather(self, city: str) -> Dict:
        """Get mock weather data"""
        conditions = ["晴朗", "多云", "阴天", "小雨", "晴转多云"]
        temps = {"Shenzhen": 22, "Beijing": 5, "Shanghai": 15}
        
        return {
            "city": city,
            "temp": temps.get(city, 20) + random.randint(-3, 3),
            "condition": random.choice(conditions),
            "humidity": random.randint(30, 70)
        }
    
    def get_all_weather(self) -> List[Dict]:
        """Get weather for all configured locations"""
        results = []
        for loc in self.config.get("locations", []):
            weather = self.get_mock_weather(loc["city"])
            weather["display_name"] = loc.get("name", loc["city"])
            results.append(weather)
        return results
    
    def format_weather_message(self, weather: Dict) -> str:
        """Format single weather as message"""
        return f"""🌤️ {weather['display_name']}
  天气: {weather['condition']}
  温度: {weather['temp']}°C
  湿度: {weather['humidity']}%"""
    
    def get_all_weather_message(self) -> str:
        """Get weather for all locations"""
        lines = [f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} 天气报告\n"]
        for weather in self.get_all_weather():
            lines.append(self.format_weather_message(weather))
            lines.append("")
        return "\n".join(lines).strip()
    
    def run(self):
        """Main execution"""
        message = self.get_all_weather_message()
        print(message)
        return message


if __name__ == "__main__":
    bot = WeatherBot()
    bot.run()
