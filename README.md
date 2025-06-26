# EmelyanovTGBot

## Стек
- Python, aiogram
- FastAPI (для webapp, если потребуется)
- npm, html, css, js (для фронтенда)
- ngrok (для проброса локального сервера)
- python-dotenv (для переменных окружения)
- Jinja2 (шаблоны)

## Запуск бота
1. Скопируйте `.env.example` в `.env` и вставьте свой Telegram Bot Token.
2. Активируйте виртуальное окружение:
   ```bash
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите бота:
   ```bash
   python bot.py
   ```

## Для разработки WebApp
- Используйте npm для фронтенда
- Запускайте ngrok для проброса локального сервера 