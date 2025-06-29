#!/bin/bash

echo "🚀 Запуск Cloudflare Tunnel для EmelyanovTGBot"
echo "================================================"

# Проверяем, установлен ли cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared не установлен!"
    echo "Установите его командой: brew install cloudflared"
    exit 1
fi

echo "✅ cloudflared найден: $(cloudflared --version)"
echo ""

# Проверяем, что сервер запущен на порту 8001
if ! curl -s http://localhost:8001 > /dev/null; then
    echo "⚠️  Сервер не запущен на порту 8001"
    echo "Сначала запустите: python server.py"
    echo ""
    echo "Хотите запустить сервер сейчас? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Запускаем сервер..."
        python server.py &
        sleep 3
    else
        echo "Запустите сервер вручную и попробуйте снова"
        exit 1
    fi
fi

echo "✅ Сервер запущен на порту 8001"
echo ""

echo "🌐 Запускаем Cloudflare Tunnel..."
echo "URL будет показан ниже. Скопируйте его и обновите WEBHOOK_URL в env.local"
echo ""

# Запускаем Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8001 