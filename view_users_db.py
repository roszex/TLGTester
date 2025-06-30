#!/usr/bin/env python3
"""
Скрипт для просмотра базы данных PostgreSQL через Railway API
"""

import requests
import json
from datetime import datetime

# URL Railway API
RAILWAY_API_URL = 'https://emelyanovtgbot-webapp-production.up.railway.app'

def get_database_stats():
    """Получает статистику базы данных"""
    try:
        # Получаем всех пользователей
        response = requests.get(f'{RAILWAY_API_URL}/api/users')
        if response.status_code != 200:
            print(f"❌ Ошибка API: {response.status_code}")
            return
        
        users = response.json()
        
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
        
        # Статистика по датам
        today = datetime.now().date()
        today_users = 0
        for user_data in users.values():
            created_at = user_data.get('created_at')
            if created_at:
                try:
                    # Парсим дату из формата "dd.mm.yyyy HH:MM:SS"
                    date_str = created_at.split()[0]
                    user_date = datetime.strptime(date_str, "%d.%m.%Y").date()
                    if user_date == today:
                        today_users += 1
                except:
                    pass
        
        print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("=" * 50)
        print(f"👥 Всего пользователей: {total_users}")
        print(f"📝 Заполнили форму: {users_with_form}")
        print(f"⏳ Не заполнили форму: {users_without_form}")
        print(f"📅 Зарегистрировались сегодня: {today_users}")
        
        print(f"\n📄 Пользователи по страницам:")
        for page in sorted(page_stats.keys()):
            print(f"   • Страница {page}: {page_stats[page]} пользователей")
        
        # Показываем последних пользователей
        print(f"\n🕒 Последние 5 пользователей:")
        sorted_users = sorted(users.items(), 
                            key=lambda x: x[1].get('created_at', ''), 
                            reverse=True)[:5]
        
        for user_id, user_data in sorted_users:
            created_at = user_data.get('created_at', 'Не указано')
            current_page = user_data.get('current_page', 1)
            has_form = "✅" if user_data.get('form_data') else "❌"
            print(f"   • {user_id} | Страница {current_page} | Форма {has_form} | {created_at}")
        
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")

def test_form_submission():
    """Тестирует отправку формы"""
    print("\n🧪 ТЕСТИРОВАНИЕ ОТПРАВКИ ФОРМЫ")
    print("=" * 50)
    
    test_user_id = f"test_user_{int(datetime.now().timestamp())}"
    test_form_data = {
        "age": "25",
        "occupation": "Тестировщик",
        "income": "50000 руб/мес",
        "motivation": "10 из 10",
        "teamwork": "9 из 10"
    }
    
    try:
        # Отправляем тестовые данные
        response = requests.post(
            f'{RAILWAY_API_URL}/api/save_form_data',
            headers={'Content-Type': 'application/json'},
            json={
                'user_id': test_user_id,
                'form_data': test_form_data
            }
        )
        
        if response.status_code == 200:
            print("✅ Тестовая форма успешно отправлена!")
            print(f"👤 Тестовый пользователь: {test_user_id}")
            
            # Проверяем, что данные сохранились
            user_response = requests.get(f'{RAILWAY_API_URL}/api/user/{test_user_id}')
            if user_response.status_code == 200:
                user_data = user_response.json()
                print("✅ Данные успешно сохранены в базе!")
                print(f"📄 Текущая страница: {user_data.get('current_page')}")
                if user_data.get('form_data'):
                    print("📝 Данные формы сохранены")
            else:
                print("❌ Не удалось получить данные пользователя")
        else:
            print(f"❌ Ошибка при отправке формы: {response.status_code}")
            print(f"Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

def main():
    print("🔍 ПРОВЕРКА БАЗЫ ДАННЫХ RAILWAY")
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
    
    # Получаем статистику
    get_database_stats()
    
    # Тестируем отправку формы
    test_form_submission()

if __name__ == "__main__":
    main() 