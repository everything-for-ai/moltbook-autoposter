# OpenClaw 部署指南

帮你快速搭建自己的 AI 助手

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/everything-for-ai/openclaw-deployment-guide.git
cd openclaw-deployment-guide

# 安装依赖
npm install -g openclaw-cli
```

### 2. 配置

```bash
# 初始化配置
openclaw init

# 编辑配置文件
openclaw config edit
```

### 3. 运行

```bash
# 启动服务
openclaw start

# 或后台运行
openclaw start -d
```

## 配置说明

```json
{
  "gateway": {
    "port": 18789,
    "auth": {
      "mode": "token",
      "token": "your-secure-token"
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "your-app-id",
      "appSecret": "your-app-secret"
    },
    "wecom": {
      "enabled": true,
      "token": "your-webhook-token"
    }
  }
}
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `openclaw start` | 启动服务 |
| `openclaw stop` | 停止服务 |
| `openclaw status` | 查看状态 |
| `openclaw logs` | 查看日志 |
| `openclaw config` | 编辑配置 |

## Docker 部署

```bash
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v openclaw-data:/data \
  openclaw/openclaw:latest
```

## 文档

- [完整文档](https://docs.openclaw.ai)
- [API 参考](https://docs.openclaw.ai/api)
- [示例项目](https://github.com/openclaw/openclaw)

## 常见问题

**Q: 端口无法访问？**
A: 检查防火墙配置，确保 18789 端口开放。

**Q: 消息收不到？**
A: 检查 channel 配置，确认 Webhook URL 正确。

**Q: 如何添加新技能？**
A: 参考 [Skill 开发文档](https://docs.openclaw.ai/skills)

## License

MIT
