# Emelyanov WebApp - GitHub Pages Version

Версия для развертывания на GitHub Pages без ограничений ngrok.

## Особенности

- ✅ **Работает в Telegram WebApp** без проблем с CORS
- ✅ **localStorage для сохранения данных** - не нужен сервер
- ✅ **Бесплатный хостинг** на GitHub Pages
- ✅ **Стабильный HTTPS URL**
- ✅ **Простая настройка**

## Быстрый старт

1. **Создайте репозиторий на GitHub**
2. **Загрузите файлы из `webapp/` в корень репозитория**
3. **Настройте GitHub Pages** (Settings → Pages)
4. **Отредактируйте `env.github`** с вашими данными
5. **Запустите бота**: `python bot.py`

## Структура проекта

```
github-pages/
├── webapp/                 # Веб-приложение
│   ├── progress.js        # Система прогресса
│   ├── page_1/           # Страницы приложения
│   ├── page_2/
│   ├── page_3/
│   └── ...
├── bot.py                # Telegram бот
├── env.github           # Конфигурация
└── requirements.txt     # Зависимости
```

## Настройка

1. **Получите токен бота** у @BotFather
2. **Создайте репозиторий** на GitHub
3. **Настройте GitHub Pages** (см. DEPLOYMENT.md)
4. **Отредактируйте `env.github`**:
   ```
   BOT_TOKEN=ваш_токен_бота
   WEBAPP_URL=https://username.github.io/repo-name/webapp/page_1/index.html
   ```

## Запуск

```bash
cd github-pages
pip install -r requirements.txt
python bot.py
```

## Преимущества над ngrok версией

- **Нет блокировок** - GitHub Pages не блокирует Telegram WebApp
- **Стабильный URL** - не меняется при перезапуске
- **Бесплатно** - не нужно платить за ngrok
- **Простота** - не нужен Flask сервер
- **Надежность** - работает стабильно

## Подробные инструкции

См. файл `DEPLOYMENT.md` для детальных инструкций по развертыванию.
