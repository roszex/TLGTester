#!/usr/bin/env python3
"""
Скрипт для просмотра данных пользователей в GitHub Pages версии
"""

import json
import os
from datetime import datetime

def load_user_data():
    """Загружает данные пользователей из JSON файла"""
    user_data_file = 'user_data.json'
    if os.path.exists(user_data_file):
        try:
            with open(user_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def display_users():
    """Отображает всех пользователей"""
    data = load_user_data()
    
    if not data:
        print("❌ Файл user_data.json не найден или пуст")
        return
    
    print(f"📊 Всего пользователей: {len(data)}")
    print("=" * 80)
    
    for user_id, user_data in data.items():
        print(f"👤 User ID: {user_id}")
        print(f"   Username: {user_data.get('username', 'Не указан')}")
        print(f"   Текущая страница: {user_data.get('current_page', 1)}")
        print(f"   Создан: {user_data.get('created_at', 'Не указано')}")
        
        form_data = user_data.get('form_data')
        if form_data:
            print("   📝 Данные формы:")
            for field, value in form_data.items():
                print(f"      {field}: {value}")
        else:
            print("   📝 Данные формы: Не заполнены")
        
        print("-" * 40)

def display_statistics():
    """Отображает статистику"""
    data = load_user_data()
    
    if not data:
        print("❌ Нет данных для статистики")
        return
    
    total_users = len(data)
    users_with_form = sum(1 for user in data.values() if user.get('form_data'))
    users_without_form = total_users - users_with_form
    
    # Статистика по страницам
    page_stats = {}
    for user in data.values():
        page = user.get('current_page', 1)
        page_stats[page] = page_stats.get(page, 0) + 1
    
    print("📈 СТАТИСТИКА:")
    print(f"   Всего пользователей: {total_users}")
    print(f"   Заполнили форму: {users_with_form}")
    print(f"   Не заполнили форму: {users_without_form}")
    print(f"   Процент заполнения: {(users_with_form/total_users)*100:.1f}%")
    
    print("\n📄 Распределение по страницам:")
    for page in sorted(page_stats.keys()):
        count = page_stats[page]
        percentage = (count/total_users)*100
        print(f"   Страница {page}: {count} пользователей ({percentage:.1f}%)")

def main():
    """Главная функция"""
    print("🔍 ПРОСМОТР ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ (GitHub Pages)")
    print("=" * 80)
    
    while True:
        print("\nВыберите действие:")
        print("1. Показать всех пользователей")
        print("2. Показать статистику")
        print("3. Выход")
        
        choice = input("\nВведите номер (1-3): ").strip()
        
        if choice == '1':
            print("\n" + "="*80)
            display_users()
        elif choice == '2':
            print("\n" + "="*80)
            display_statistics()
        elif choice == '3':
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    main() 