# Развертывание на GitHub Pages

## Шаги для развертывания:

### 1. Создайте репозиторий на GitHub
- Создайте новый репозиторий
- Назовите его, например: `emelyanov-webapp`

### 2. Загрузите файлы
- Скопируйте все файлы из папки `github-pages/webapp/` в корень репозитория
- Или создайте папку `webapp/` и поместите туда файлы

### 3. Настройте GitHub Pages
- Перейдите в Settings → Pages
- В разделе "Source" выберите "Deploy from a branch"
- Выберите ветку `main` и папку `/` (или `/webapp` если файлы в папке)
- Нажмите "Save"

### 4. Получите URL
- GitHub Pages будет доступен по адресу: `https://your-username.github.io/emelyanov-webapp/`
- Если файлы в папке webapp: `https://your-username.github.io/emelyanov-webapp/webapp/`

### 5. Настройте бота
- Отредактируйте файл `env.github`:
  ```
  BOT_TOKEN=ваш_токен_бота
  WEBAPP_URL=https://your-username.github.io/emelyanov-webapp/webapp/page_1/index.html
  ```

### 6. Запустите бота
```bash
cd github-pages
python bot.py
```

## Преимущества GitHub Pages:

✅ **Нет ограничений ngrok** - работает без проблем с Telegram WebApp  
✅ **Бесплатный хостинг** - не нужно платить за ngrok  
✅ **Стабильный URL** - не меняется при перезапуске  
✅ **HTTPS по умолчанию** - безопасное соединение  
✅ **Быстрая загрузка** - CDN от GitHub  

## Структура файлов:

```
github-pages/
├── webapp/
│   ├── progress.js          # Система прогресса (localStorage)
│   ├── page_1/
│   ├── page_2/
│   ├── page_3/
│   └── ...
├── bot.py                   # Telegram бот
├── env.github              # Переменные окружения
├── requirements.txt        # Зависимости Python
└── README.md              # Документация
```

## Примечания:

- **localStorage**: Данные сохраняются в браузере пользователя
- **Нет сервера**: Не нужен Flask сервер
- **Простота**: Минимум зависимостей и настроек
- **Надежность**: Работает стабильно в Telegram WebApp 