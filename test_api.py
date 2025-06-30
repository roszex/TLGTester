import requests
import json

# Тестируем Railway API
BASE_URL = "https://emelyanovtgbot-webapp-production.up.railway.app"

def test_api():
    user_id = "test_user_123"
    
    print("=== Тестирование Railway API ===")
    print(f"Base URL: {BASE_URL}")
    
    # 1. Проверяем доступность сервера
    print("\n1. Проверяем доступность сервера...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # 2. Получаем данные пользователя
    print("\n2. Получаем данные пользователя...")
    try:
        response = requests.get(f"{BASE_URL}/api/user/{user_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. Сохраняем прогресс
    print("\n3. Сохраняем прогресс...")
    try:
        response = requests.post(f"{BASE_URL}/api/save_progress", 
                               json={
                                   "user_id": user_id,
                                   "current_page": 5
                               })
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 4. Сохраняем данные формы
    print("\n4. Сохраняем данные формы...")
    form_data = {
        "age": "25",
        "occupation": "Тестировщик",
        "income": "60000 руб/мес",
        "motivation": "8 из 10",
        "teamwork": "Готов к командной работе"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/user/{user_id}", 
                               json={"form_data": form_data})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 5. Получаем прогресс
    print("\n5. Получаем прогресс...")
    try:
        response = requests.get(f"{BASE_URL}/api/get_progress/{user_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 6. Получаем всех пользователей
    print("\n6. Получаем всех пользователей...")
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api() 