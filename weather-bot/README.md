# Weather Bot

Multi-platform weather notification bot - supports WeChat, Telegram, Slack, and more.

## Features

- 📍 Multi-location weather updates
- 🌡️ Temperature, humidity, and conditions
- 🔔 Customizable alerts
- 📅 Scheduled notifications

## Setup

```bash
# Clone the repo
git clone https://github.com/everything-for-ai/weather-bot.git
cd weather-bot

# Install dependencies
pip install -r requirements.txt

# Configure
cp config.example.json config.json
# Edit config.json with your API keys

# Run
python weather_bot.py
```

## Configuration

```json
{
    "locations": [
        {"name": "深圳", "city": "Shenzhen"},
        {"name": "北京", "city": "Beijing"}
    ],
    "schedule": "08:00",
    "platforms": ["feishu", "wecom"],
    "weather_api_key": "your-api-key"
}
```

## Cron Jobs

```bash
# Morning weather report at 8 AM
0 8 * * * cd /path/to/weather-bot && python weather_bot.py >> /var/log/weather.log 2>&1
```

## API

```python
from weather import WeatherBot

bot = WeatherBot()
bot.send_weather("深圳")
```

## License

MIT
