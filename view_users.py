#!/usr/bin/env python3
"""
Скрипт для просмотра пользователей из PostgreSQL базы данных Railway
"""

import os
import requests
import json
from datetime import datetime

# URL Railway API
RAILWAY_API_URL = 'https://emelyanovtgbot-webapp-production.up.railway.app'

def get_users_from_api():
    """Получает пользователей через API"""
    try:
        response = requests.get(f'{RAILWAY_API_URL}/api/users')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка API: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return {}

def display_users(users):
    """Отображает пользователей в красивом формате"""
    if not users:
        print("Пользователей не найдено!")
        return
    
    print(f"\n📊 Найдено пользователей: {len(users)}")
    print("=" * 80)
    
    for user_id, user_data in users.items():
        print(f"\n👤 Пользователь: {user_id}")
        print(f"📅 Создан: {user_data.get('created_at', 'Не указано')}")
        print(f"📄 Текущая страница: {user_data.get('current_page', 1)}")
        
        form_data = user_data.get('form_data')
        if form_data:
            print("📝 Данные формы:")
            print(f"   • Возраст: {form_data.get('age', 'Не указано')}")
            print(f"   • Род деятельности: {form_data.get('occupation', 'Не указано')}")
            print(f"   • Доход: {form_data.get('income', 'Не указано')}")
            print(f"   • Мотивация: {form_data.get('motivation', 'Не указано')}")
            print(f"   • Командная работа: {form_data.get('teamwork', 'Не указано')}")
        else:
            print("📝 Данные формы: Не заполнены")
        
        print("-" * 40)

def get_user_stats(users):
    """Показывает статистику пользователей"""
    if not users:
        print("Нет данных для статистики!")
        return
    
    total_users = len(users)
    users_with_form = sum(1 for u in users.values() if u.get('form_data'))
    avg_page = sum(u.get('current_page', 1) for u in users.values()) / total_users
    
    print(f"\n📈 Статистика:")
    print(f"   • Всего пользователей: {total_users}")
    print(f"   • Заполнили форму: {users_with_form}")
    print(f"   • Не заполнили форму: {total_users - users_with_form}")
    print(f"   • Средняя страница: {avg_page:.1f}")
    
    # Статистика по страницам
    page_stats = {}
    for user_data in users.values():
        page = user_data.get('current_page', 1)
        page_stats[page] = page_stats.get(page, 0) + 1
    
    print(f"\n📄 Пользователи по страницам:")
    for page in sorted(page_stats.keys()):
        print(f"   • Страница {page}: {page_stats[page]} пользователей")

def main():
    print("🔍 Получение данных пользователей из Railway PostgreSQL...")
    
    users = get_users_from_api()
    
    if users:
        display_users(users)
        get_user_stats(users)
    else:
        print("❌ Не удалось получить данные пользователей")

if __name__ == "__main__":
    main() 