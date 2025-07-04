# TLGTester - Telegram Lead Generator

## Описание
Telegram WebApp для сбора лидов с автоматическими уведомлениями админу и сохранением данных в JSON.

## Функциональность
- 📱 Интерактивное веб-приложение в Telegram
- 📊 Сбор данных через форму
- 🎯 Автоматические уведомления админу о новых лидах
- 💾 Сохранение всех лидов в JSON файл
- 📈 Экспорт данных в CSV

## Структура проекта
```
├── bot.py              # Telegram бот
├── view_leads.py       # Скрипт просмотра лидов
├── requirements.txt    # Зависимости Python
├── leads.json         # Файл с лидами (создается автоматически)
├── outro_image.JPG    # Фото для финального сообщения
└── webapp/            # Веб-приложение
    ├── page_1/        # Главная страница
    ├── page_2/        # Страница с фото
    ├── page_3/        # Контактная форма
    ├── page_4/        # Конец ознакомительной части
    └── progress.js    # Менеджер прогресса
```

## Настройка

### 1. Создайте .env файл
```bash
# Telegram Bot Token (получить у @BotFather)
BOT_TOKEN=your_bot_token_here

# URL веб-приложения (GitHub Pages или другой HTTPS сервер)
WEBAPP_URL=https://roszex.github.io/TLGTester/webapp/page_1/index.html

# ID админа для уведомлений о новых лидах (ваш Telegram ID)
ADMIN_ID=8054389212
```

### 2. Установите зависимости
```bash
pip install -r requirements.txt
```

### 3. Запустите бота
```bash
python bot.py
```

## Развертывание на Beget

### 1. Загрузите файлы на Beget
- Загрузите все файлы в папку на хостинге
- Убедитесь, что файлы имеют права на запись (644 для файлов, 755 для папок)

### 2. Настройте Python на Beget
- В панели Beget создайте Python приложение
- Укажите путь к `bot.py` как точку входа
- Установите Python 3.8+ если нужно

### 3. Настройте переменные окружения
- В панели Beget добавьте переменные:
  - `BOT_TOKEN`
  - `WEBAPP_URL` 
  - `ADMIN_ID`

### 4. Запустите приложение
- В панели Beget запустите Python приложение
- Бот будет работать в фоновом режиме

## Работа с лидами

### Просмотр лидов
```bash
python view_leads.py
```

### Экспорт в CSV
```bash
python view_leads.py
# Выберите опцию 2
```

### Уведомления админу
При каждом новом лиде админ получает сообщение:
```
🎯 Лид #1
👤 @username
⏰ 03.07 14:30
```

## Важные моменты для Beget

### 1. Файл leads.json
- ✅ **Будет сохраняться и обновляться** на Beget
- ✅ **Данные не потеряются** при перезапуске
- ⚠️ **Рекомендуется** делать резервные копии

### 2. Права доступа
```bash
chmod 644 bot.py
chmod 644 view_leads.py
chmod 666 leads.json  # Для записи
```

### 3. Логирование
- Логи бота сохраняются в стандартном выводе
- На Beget можно настроить ротацию логов

### 4. Автозапуск
- Настройте автозапуск бота при перезагрузке сервера
- Используйте systemd или supervisor

## Команды бота

- `/start` - Запуск WebApp
- `/leads` - Просмотр статистики (можно добавить)

## Безопасность

- ✅ Все данные передаются через HTTPS
- ✅ Telegram WebApp безопасен
- ⚠️ Храните BOT_TOKEN в секрете
- ⚠️ Регулярно делайте бэкапы leads.json

## Поддержка

- Telegram: @desperatecoder
- Канал: https://t.me/desperateecoder 