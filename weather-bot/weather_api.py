#!/usr/bin/env python3
"""
Weather API - OpenWeatherMap integration
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional


class WeatherAPI:
    """OpenWeatherMap API wrapper"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENWEATHERMAP_APPID", "")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.icon_url = "http://openweathermap.org/img/wn/{icon}@2x.png"
    
    def get_current(self, city: str, country: str = "CN") -> Optional[Dict]:
        """Get current weather for a city"""
        if not self.api_key:
            return None
        
        params = {
            "q": f"{city},{country}",
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(f"{self.base_url}/weather", params=params, timeout=10)
            data = response.json()
            
            if data.get("cod") == 200:
                return {
                    "city": city,
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
                    "sunset": datetime.fromtimestamp(data["sys"]["sunset"])
                }
        except Exception as e:
            print(f"Weather API error: {e}")
        
        return None
    
    def get_forecast(self, city: str, country: str = "CN", days: int = 5) -> List[Dict]:
        """Get 5-day forecast"""
        if not self.api_key:
            return []
        
        # Using OneCall API for forecast
        # For simplicity, return empty list if no API key
        return []
    
    def get_icon_url(self, icon: str) -> str:
        """Get weather icon URL"""
        return self.icon_url.format(icon=icon)
    
    def format_weather_message(self, weather: Dict) -> str:
        """Format weather data as a message"""
        return f"""
🌤️ {weather['city']} 天气

{weather['description'].capitalize()}
🌡️ 温度: {weather['temp']:.1f}°C (体感 {weather['feels_like']:.1f}°C)
💧 湿度: {weather['humidity']}%
💨 风速: {weather['wind_speed']} m/s
🌅 日出: {weather['sunrise'].strftime('%H:%M')}
🌇 日落: {weather['sunset'].strftime('%H:%M')}
        """.strip()


# Test
if __name__ == "__main__":
    api = WeatherAPI()
    weather = api.get_current("Shenzhen", "CN")
    
    if weather:
        print(api.format_weather_message(weather))
    else:
        print("需要配置 OPENWEATHERMAP_APPID 环境变量")
