# EmelyanovTGBot - Local ngrok Version

Версия для локального запуска через ngrok.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения в файле `env.local`:
```
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://your-ngrok-url.ngrok.io
PORT=8000
```

## Запуск

1. Запустите ngrok:
```bash
ngrok http 8000
```

2. Скопируйте HTTPS URL из ngrok (например: https://abc123.ngrok.io)

3. Обновите `WEBAPP_URL` в файле `env.local` с вашим ngrok URL

4. Запустите сервер:
```bash
python server.py
```

5. Запустите бота:
```bash
python bot.py
```

## Структура

- `env.local` - переменные окружения для локального запуска
- `bot.py` - Telegram бот
- `server.py` - Flask сервер для веб-приложения
- `requirements.txt` - зависимости Python 