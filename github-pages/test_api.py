#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API GitHub Pages версии
"""

import requests
import json
import time

# Базовый URL для GitHub Pages (замените на ваш)
BASE_URL = "http://localhost:8002"  # Для локального тестирования

def test_get_user_data(user_id):
    """Тестирует получение данных пользователя"""
    print(f"🔍 Тестируем GET /api/user/{user_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/user/{user_id}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def test_update_user_data(user_id, data):
    """Тестирует обновление данных пользователя"""
    print(f"📝 Тестируем POST /api/user/{user_id}")
    print(f"   Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/user/{user_id}",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def test_save_progress(user_id, current_page, form_data=None):
    """Тестирует сохранение прогресса"""
    print(f"💾 Тестируем POST /api/save_progress")
    
    data = {
        'user_id': user_id,
        'current_page': current_page
    }
    
    if form_data:
        data['form_data'] = form_data
    
    print(f"   Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/save_progress",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def test_get_progress(user_id):
    """Тестирует получение прогресса"""
    print(f"📊 Тестируем GET /api/get_progress/{user_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/get_progress/{user_id}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def test_get_all_users():
    """Тестирует получение всех пользователей"""
    print(f"👥 Тестируем GET /api/users")
    
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Всего пользователей: {len(data)}")
            print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def main():
    """Главная функция тестирования"""
    print("🧪 ТЕСТИРОВАНИЕ API (GitHub Pages)")
    print("=" * 60)
    
    # Тестовые данные
    test_user_id = "test_user_github_pages"
    test_form_data = {
        "age": "25",
        "occupation": "Тестировщик GitHub Pages",
        "income": "80000 руб/мес",
        "motivation": "9 из 10",
        "teamwork": "Готов к командной работе"
    }
    
    print(f"🌐 Базовый URL: {BASE_URL}")
    print(f"👤 Тестовый User ID: {test_user_id}")
    print()
    
    # Тест 1: Получение данных пользователя (создаст нового)
    test_get_user_data(test_user_id)
    print()
    
    # Тест 2: Обновление данных пользователя
    test_update_user_data(test_user_id, {
        'username': '@test_github_pages',
        'current_page': 5
    })
    print()
    
    # Тест 3: Сохранение прогресса с формой
    test_save_progress(test_user_id, 7, test_form_data)
    print()
    
    # Тест 4: Получение прогресса
    test_get_progress(test_user_id)
    print()
    
    # Тест 5: Получение всех пользователей
    test_get_all_users()
    print()
    
    print("✅ Тестирование завершено!")

if __name__ == '__main__':
    main() 