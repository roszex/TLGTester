# EmelyanovTGBot - Local ngrok Version

Версия для локального запуска через ngrok.


установка виртуалки

установка в виртуалку зависимостей из requirements.txt

```bash
pip install -r requirements.txt
```


```

2. Создайте файл `.env` вручную. Настройте переменные окружения в файле `.env`:
```
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://roszex.github.io/EmelyanovTGBot-webapp
```

## Запуск



5. Запустите бота:
```bash
python bot.py
```

## Структура

- `.env` - переменные окружения для локального запуска
- `bot.py` - Telegram бот
- `requirements.txt` - зависимости Python 