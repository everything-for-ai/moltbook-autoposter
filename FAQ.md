# Everything for AI - 常见问题

## Q1: 如何运行这些项目？

```bash
# 克隆项目
git clone https://github.com/everything-for-ai/<project-name>.git
cd <project-name>

# 安装依赖
pip install -r requirements.txt

# 运行
python *.py
```

## Q2: 如何配置 API Key？

大部分项目需要配置 API Key，有两种方式：

**方式一：环境变量**
```bash
export OPENAI_API_KEY="your-key"
export OPENWEATHERMAP_APPID="your-key"
```

**方式二：配置文件**
```bash
cp config.example.json config.json
# 编辑 config.json 填入你的 API Key
```

## Q3: 如何在服务器上定时运行？

使用 cron 定时任务：

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天 8 点运行天气机器人）
0 8 * * * cd /path/to/weather-bot && python weather_bot.py >> /var/log/weather.log 2>&1
```

## Q4: 如何部署到生产环境？

### Docker 部署
```bash
docker build -t everything-for-ai/weather-bot .
docker run -d -p 8080:8080 everything-for-ai/weather-bot
```

### Systemd 服务
```bash
# /etc/systemd/system/weather-bot.service
[Unit]
Description=Weather Bot Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/weather-bot
ExecStart=/usr/bin/python3 weather_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Q5: 如何为项目贡献代码？

1. Fork 项目
2. 创建分支 (`git checkout -b feature/new-feature`)
3. 提交改动 (`git commit -m "Add new feature"`)
4. 推送到分支 (`git push origin feature/new-feature`)
5. 创建 Pull Request

## Q6: 遇到问题怎么办？

1. 查看项目 README
2. 查看 issues 是否有人遇到同样问题
3. 新建 issue 描述你的问题
4. 提 PR 修复问题

## Q7: 支持哪些消息平台？

- 飞书 (Feishu)
- 企业微信 (WeCom)
- Telegram
- Slack

具体配置请参考各项目的 config.json.example

## Q8: 如何添加新的消息平台？

参考现有平台的实现，主要实现两个方法：
- `send_message()` - 发送消息
- `parse_message()` - 解析接收的消息
