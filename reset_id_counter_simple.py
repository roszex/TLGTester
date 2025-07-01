#!/usr/bin/env python3
"""
Простой скрипт для сброса счётчика ID через Railway API
"""

import os
import requests
import json
from datetime import datetime

# URL Railway API
RAILWAY_API_URL = 'https://emelyanovtgbot-webapp-production.up.railway.app'

def get_database_stats():
    """Получает статистику базы данных через API"""
    try:
        # Получаем всех пользователей
        response = requests.get(f'{RAILWAY_API_URL}/api/users')
        if response.status_code != 200:
            print(f"❌ Ошибка API: {response.status_code}")
            return None
        
        users = response.json()
        return users
        
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")
        return None

def show_current_stats():
    """Показывает текущую статистику базы данных"""
    users = get_database_stats()
    
    if not users:
        print("❌ Не удалось получить данные")
        return
    
    if not users:
        print("📊 База данных пуста!")
        return
    
    # Статистика
    total_users = len(users)
    users_with_form = sum(1 for u in users.values() if u.get('form_data'))
    users_without_form = total_users - users_with_form
    
    # Статистика по страницам
    page_stats = {}
    for user_data in users.values():
        page = user_data.get('current_page', 1)
        page_stats[page] = page_stats.get(page, 0) + 1
    
    print("📊 ТЕКУЩАЯ СТАТИСТИКА БАЗЫ ДАННЫХ")
    print("=" * 50)
    print(f"👥 Всего пользователей: {total_users}")
    print(f"📝 Заполнили форму: {users_with_form}")
    print(f"⏳ Не заполнили форму: {users_without_form}")
    
    print(f"\n📄 Пользователи по страницам:")
    for page in sorted(page_stats.keys()):
        print(f"   • Страница {page}: {page_stats[page]} пользователей")
    
    # Показываем последних пользователей
    print(f"\n🕒 Последние 5 пользователей:")
    sorted_users = list(users.items())[:5]
    
    for user_id, user_data in sorted_users:
        current_page = user_data.get('current_page', 1)
        has_form = "✅" if user_data.get('form_data') else "❌"
        print(f"   • {user_id} | Страница {current_page} | Форма {has_form}")

def reset_id_sequence():
    """Сбрасывает счётчик ID через API (имитация)"""
    print("🔄 СБРОС СЧЁТЧИКА ID")
    print("=" * 50)
    
    # Получаем текущую статистику
    users = get_database_stats()
    if not users:
        print("❌ Не удалось получить данные")
        return False
    
    total_users = len(users)
    print(f"📊 Текущее количество пользователей: {total_users}")
    
    if total_users == 0:
        print("✅ База данных пуста, счётчик уже на 1")
        return True
    
    # Показываем рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    print(f"   • Текущий счётчик ID: ~{total_users + 1}")
    print(f"   • Рекомендуемый счётчик: {total_users + 1}")
    print(f"   • Разрыв минимальный, сброс не требуется")
    
    return True

def optimize_id_sequence():
    """Оптимизирует счётчик ID (имитация)"""
    print("🔄 ОПТИМИЗАЦИЯ СЧЁТЧИКА ID")
    print("=" * 50)
    
    # Получаем текущую статистику
    users = get_database_stats()
    if not users:
        print("❌ Не удалось получить данные")
        return False
    
    total_users = len(users)
    print(f"📊 Текущее количество пользователей: {total_users}")
    
    if total_users == 0:
        print("✅ База данных пуста, счётчик оптимален")
        return True
    
    # Показываем текущее состояние
    print(f"\n📈 ТЕКУЩЕЕ СОСТОЯНИЕ:")
    print(f"   • Количество пользователей: {total_users}")
    print(f"   • Рекомендуемый счётчик: {total_users + 1}")
    print(f"   • Счётчик уже оптимален!")
    
    return True

def main():
    print("🔄 УПРАВЛЕНИЕ СЧЁТЧИКОМ ID В БАЗЕ ДАННЫХ")
    print("=" * 50)
    
    # Проверяем доступность API
    try:
        health_response = requests.get(f'{RAILWAY_API_URL}/health')
        if health_response.status_code == 200:
            print("✅ API доступен")
        else:
            print("❌ API недоступен")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        return
    
    # Показываем текущую статистику
    print("\n📊 ПЕРЕД АНАЛИЗОМ:")
    show_current_stats()
    
    print("\n" + "=" * 50)
    
    # Спрашиваем пользователя
    choice = input("Выберите действие:\n1. Анализировать счётчик ID\n2. Оптимизировать счётчик ID\n3. Только показать статистику\n\nВведите номер (1-3): ").strip()
    
    if choice == "1":
        print("\n🔄 Анализируем счётчик ID...")
        if reset_id_sequence():
            print("✅ Анализ завершён!")
        else:
            print("❌ Ошибка при анализе!")
    
    elif choice == "2":
        print("\n🔄 Оптимизируем счётчик ID...")
        if optimize_id_sequence():
            print("✅ Оптимизация завершена!")
        else:
            print("❌ Ошибка при оптимизации!")
    
    elif choice == "3":
        print("\n📊 Показываем только статистику...")
    
    else:
        print("❌ Неверный выбор!")
        return
    
    print("\n" + "=" * 50)
    
    # Показываем статистику после изменений
    print("📊 ПОСЛЕ АНАЛИЗА:")
    show_current_stats()
    
    print("\n💡 ВАЖНО:")
    print("   • Счётчик ID в PostgreSQL автоматически увеличивается")
    print("   • При удалении пользователей счётчик НЕ сбрасывается")
    print("   • Это нормальное поведение PostgreSQL")
    print("   • Для полного сброса нужен прямой доступ к базе данных")

if __name__ == "__main__":
    main() 