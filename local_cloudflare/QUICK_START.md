# 🚀 Быстрый старт - Cloudflare Tunnel

## 1. Установка Cloudflare Tunnel

```bash
# macOS
brew install cloudflared

# Проверка установки
cloudflared --version
```

## 2. Настройка проекта

```bash
cd local_cloudflare

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

## 3. Настройка переменных окружения

Отредактируйте `env.local`:
```env
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_URL=https://your-cloudflare-domain.trycloudflare.com
PORT=8001
```

## 4. Запуск (3 терминала)

### Терминал 1: Сервер
```bash
python server.py
```

### Терминал 2: Cloudflare Tunnel
```bash
./start_cloudflare.sh
# или
cloudflared tunnel --url http://localhost:8001
```

### Терминал 3: Бот
```bash
python bot.py
```

## 5. Получение URL

После запуска Cloudflare Tunnel вы получите URL типа:
```
https://abc123-def456-ghi789.trycloudflare.com
```

Скопируйте его и обновите `WEBHOOK_URL` в `env.local`.

## 6. Тестирование

1. Отправьте `/start` боту
2. Откройте веб-приложение
3. Проверьте, что картинки отображаются
4. Заполните форму и проверьте сохранение

## ✅ Готово!

Теперь у вас стабильный HTTPS URL без проблем ngrok! 🎉 