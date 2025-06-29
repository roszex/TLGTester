import requests
import json

# Тестируем API сервера
BASE_URL = "http://localhost:8001"

def test_api():
    user_id = "test_user_123"
    
    print("=== Тестирование API ===")
    
    # 1. Получаем данные пользователя
    print("\n1. Получаем данные пользователя...")
    try:
        response = requests.get(f"{BASE_URL}/api/user/{user_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Обновляем прогресс
    print("\n2. Обновляем прогресс...")
    try:
        response = requests.post(f"{BASE_URL}/api/progress/{user_id}", 
                               json={"page": 5})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. Сохраняем данные формы
    print("\n3. Сохраняем данные формы...")
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
    
    # 4. Проверяем обновленные данные
    print("\n4. Проверяем обновленные данные...")
    try:
        response = requests.get(f"{BASE_URL}/api/user/{user_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api() 