# Daily Report Generator

AI-powered daily work report generator - generates summaries from git commits, tasks, and notes.

## Features

- 📊 Git commit history analysis
- ✅ Task completion tracking
- 📝 Meeting notes integration
- 🤖 AI-powered summary generation
- 📤 Multi-platform delivery (Feishu, WeCom, Telegram)

## Quick Start

```bash
# Clone
git clone https://github.com/everything-for-ai/daily-report-generator.git
cd daily-report-generator

# Install
pip install -r requirements.txt

# Configure
cp config.example.json config.json
# Edit config.json with your OpenAI API key

# Run
python daily.py
```

## Configuration

```json
{
  "openai_api_key": "your-api-key",
  "model": "gpt-3.5-turbo",
  "include_git_commits": true,
  "include_tasks": true,
  "output_format": "markdown"
}
```

## Scheduled Execution

```bash
# Run at 10 AM every workday
0 10 * * 1-5 cd /path/to/daily-report-generator && python daily.py
```

## Project Structure

```
daily-report-generator/
├── daily.py           # Main entry point
├── config.json        # Configuration
├── requirements.txt   # Dependencies
├── README.md          # This file
└── reports/           # Generated reports
```

## API Usage

```python
from daily import DailyReportGenerator

generator = DailyReportGenerator()
report = generator.run()
print(report)
```

## License

MIT
