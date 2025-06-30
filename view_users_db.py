#!/usr/bin/env python3
"""
Скрипт для просмотра данных пользователей из PostgreSQL базы данных
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def get_db_connection():
    """Получает соединение с базой данных"""
    try:
        # Получаем переменные окружения от Railway
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            # Railway предоставляет DATABASE_URL в формате postgresql://user:pass@host:port/db
            conn = psycopg2.connect(database_url)
        else:
            # Fallback для локальной разработки
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'emelyanov_bot'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', ''),
                port=os.getenv('DB_PORT', '5432')
            )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def view_users():
    """Показывает данные всех пользователей"""
    conn = get_db_connection()
    if not conn:
        print("Не удалось подключиться к базе данных!")
        return
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('''
            SELECT u.*, f.age, f.occupation, f.income, f.motivation, f.teamwork
            FROM users u
            LEFT JOIN form_data f ON u.user_id = f.user_id
            ORDER BY u.created_at DESC
        ''')
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not results:
            print("Нет данных пользователей!")
            return
        
        print(f"Всего пользователей: {len(results)}")
        print("=" * 80)
        
        for row in results:
            user_data = dict(row)
            print(f"ID: {user_data['user_id']}")
            print(f"Username: {user_data.get('username', 'Не указан')}")
            print(f"Текущая страница: {user_data.get('current_page', 1)}")
            
            # Показываем время создания
            created_at = user_data.get('created_at')
            if created_at:
                print(f"Создан: {created_at.strftime('%d.%m.%Y %H:%M:%S')}")
            
            # Показываем данные формы
            if user_data.get('age') or user_data.get('occupation'):
                print("Данные формы:")
                print(f"  Возраст: {user_data.get('age', 'Не указан')}")
                print(f"  Род деятельности: {user_data.get('occupation', 'Не указан')}")
                print(f"  Доход: {user_data.get('income', 'Не указан')}")
                print(f"  Мотивация: {user_data.get('motivation', 'Не указан')}")
                print(f"  Работа в команде: {user_data.get('teamwork', 'Не указан')}")
            else:
                print("Данные формы: Не заполнены")
            
            print("-" * 80)
            
    except Exception as e:
        print(f"Ошибка чтения базы данных: {e}")

def view_user_by_username(username):
    """Показывает данные конкретного пользователя по username"""
    conn = get_db_connection()
    if not conn:
        print("Не удалось подключиться к базе данных!")
        return
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('''
            SELECT u.*, f.age, f.occupation, f.income, f.motivation, f.teamwork
            FROM users u
            LEFT JOIN form_data f ON u.user_id = f.user_id
            WHERE u.username = %s
        ''', (username,))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            user_data = dict(result)
            print(f"Найден пользователь: {username}")
            print("=" * 50)
            print(f"ID: {user_data['user_id']}")
            print(f"Текущая страница: {user_data.get('current_page', 1)}")
            
            # Показываем время создания
            created_at = user_data.get('created_at')
            if created_at:
                print(f"Создан: {created_at.strftime('%d.%m.%Y %H:%M:%S')}")
            
            # Показываем данные формы
            if user_data.get('age') or user_data.get('occupation'):
                print("Данные формы:")
                print(f"  Возраст: {user_data.get('age', 'Не указан')}")
                print(f"  Род деятельности: {user_data.get('occupation', 'Не указан')}")
                print(f"  Доход: {user_data.get('income', 'Не указан')}")
                print(f"  Мотивация: {user_data.get('motivation', 'Не указан')}")
                print(f"  Работа в команде: {user_data.get('teamwork', 'Не указан')}")
            else:
                print("Данные формы: Не заполнены")
        else:
            print(f"Пользователь {username} не найден!")
            
    except Exception as e:
        print(f"Ошибка чтения базы данных: {e}")

def get_database_stats():
    """Показывает статистику базы данных"""
    conn = get_db_connection()
    if not conn:
        print("Не удалось подключиться к базе данных!")
        return
    
    try:
        cursor = conn.cursor()
        
        # Общее количество пользователей
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        # Пользователи с заполненными формами
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM form_data')
        users_with_forms = cursor.fetchone()[0]
        
        # Последние 5 пользователей
        cursor.execute('SELECT user_id, username, created_at FROM users ORDER BY created_at DESC LIMIT 5')
        recent_users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        print("=== Статистика базы данных ===")
        print(f"Всего пользователей: {total_users}")
        print(f"Пользователей с формами: {users_with_forms}")
        print(f"Пользователей без форм: {total_users - users_with_forms}")
        print("\nПоследние 5 пользователей:")
        for user in recent_users:
            print(f"  {user[0]} (@{user[1] or 'без username'}) - {user[2].strftime('%d.%m.%Y %H:%M:%S')}")
            
    except Exception as e:
        print(f"Ошибка получения статистики: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "stats":
            get_database_stats()
        else:
            # Если передан username, показываем конкретного пользователя
            username = sys.argv[1]
            view_user_by_username(username)
    else:
        # Иначе показываем всех пользователей
        view_users() 