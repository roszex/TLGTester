#!/usr/bin/env python3
"""
Скрипт для просмотра данных пользователей из JSON файла
"""

import json
import os
from datetime import datetime

def view_users():
    """Показывает данные всех пользователей"""
    user_data_file = 'user_data.json'
    
    if not os.path.exists(user_data_file):
        print("Файл user_data.json не найден!")
        return
    
    try:
        with open(user_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Ошибка чтения JSON файла!")
        return
    
    if not data:
        print("Нет данных пользователей!")
        return
    
    print(f"Всего пользователей: {len(data)}")
    print("=" * 80)
    
    for user_id, user_data in data.items():
        print(f"ID: {user_id}")
        print(f"Username: {user_data.get('username', 'Не указан')}")
        print(f"Текущая страница: {user_data.get('current_page', 1)}")
        
        # Показываем время создания
        created_at = user_data.get('created_at')
        if created_at:
            print(f"Создан: {created_at}")
        
        # Показываем данные формы
        form_data = user_data.get('form_data')
        if form_data:
            print("Данные формы:")
            print(f"  Возраст: {form_data.get('age', 'Не указан')}")
            print(f"  Род деятельности: {form_data.get('occupation', 'Не указан')}")
            print(f"  Доход: {form_data.get('income', 'Не указан')}")
            print(f"  Мотивация: {form_data.get('motivation', 'Не указан')}")
            print(f"  Работа в команде: {form_data.get('teamwork', 'Не указан')}")
        else:
            print("Данные формы: Не заполнены")
        
        print("-" * 80)

def view_user_by_username(username):
    """Показывает данные конкретного пользователя по username"""
    user_data_file = 'user_data.json'
    
    if not os.path.exists(user_data_file):
        print("Файл user_data.json не найден!")
        return
    
    try:
        with open(user_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Ошибка чтения JSON файла!")
        return
    
    # Ищем пользователя по username
    for user_id, user_data in data.items():
        if user_data.get('username') == username:
            print(f"Найден пользователь: {username}")
            print("=" * 50)
            print(f"ID: {user_id}")
            print(f"Текущая страница: {user_data.get('current_page', 1)}")
            
            # Показываем время создания
            created_at = user_data.get('created_at')
            if created_at:
                print(f"Создан: {created_at}")
            
            # Показываем данные формы
            form_data = user_data.get('form_data')
            if form_data:
                print("Данные формы:")
                print(f"  Возраст: {form_data.get('age', 'Не указан')}")
                print(f"  Род деятельности: {form_data.get('occupation', 'Не указан')}")
                print(f"  Доход: {form_data.get('income', 'Не указан')}")
                print(f"  Мотивация: {form_data.get('motivation', 'Не указан')}")
                print(f"  Работа в команде: {form_data.get('teamwork', 'Не указан')}")
            else:
                print("Данные формы: Не заполнены")
            
            return
    
    print(f"Пользователь {username} не найден!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Если передан username, показываем конкретного пользователя
        username = sys.argv[1]
        view_user_by_username(username)
    else:
        # Иначе показываем всех пользователей
        view_users() 