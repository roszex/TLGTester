#!/usr/bin/env python3
"""
Скрипт для миграции старых данных JSON
"""

import json
import os
from datetime import datetime

def get_readable_datetime(iso_string):
    """Конвертирует ISO строку в читаемый формат"""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y %H:%M:%S")
    except:
        return iso_string

def migrate_data():
    """Мигрирует данные в новый формат"""
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
    
    print(f"Найдено {len(data)} пользователей для миграции...")
    
    migrated_count = 0
    for user_id, user_data in data.items():
        print(f"Мигрируем пользователя: {user_id}")
        
        # Удаляем лишние поля
        if 'last_visited' in user_data:
            del user_data['last_visited']
            print(f"  - Удален last_visited")
        
        # Обновляем created_at если нужно
        if 'created_at' in user_data:
            old_created_at = user_data['created_at']
            if 'T' in old_created_at:  # Если это ISO формат
                user_data['created_at'] = get_readable_datetime(old_created_at)
                print(f"  - Обновлен created_at: {old_created_at} -> {user_data['created_at']}")
        
        # Очищаем данные формы
        if user_data.get('form_data'):
            form_data = user_data['form_data']
            if 'timestamp' in form_data:
                del form_data['timestamp']
                print(f"  - Удален timestamp из формы")
            if 'userAgent' in form_data:
                del form_data['userAgent']
                print(f"  - Удален userAgent из формы")
        
        migrated_count += 1
    
    # Сохраняем обновленные данные
    with open(user_data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nМиграция завершена! Обработано {migrated_count} пользователей.")
    print("Файл user_data.json обновлен.")

if __name__ == "__main__":
    migrate_data() 