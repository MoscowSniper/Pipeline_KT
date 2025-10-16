# CI/CD Pipeline App

Flask application with automated CI/CD pipeline.

## Features
- REST API
- Version endpoint
- Automated deployments

## Usage
```bash
docker run -p 8000:8000 yourname/pipeline-app:latest

## 3. Настройте Secrets в GitHub:

Нужны следующие secrets:
- `DOCKER_USERNAME` - ваш Docker Hub username
- `DOCKER_PASSWORD` - ваш Docker Hub password/token
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота
- `TELEGRAM_CHAT_ID` - ID чата для уведомлений

## 4. Ссылка на телеграмм группу:
https://t.me/tbapipe
