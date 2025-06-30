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
        
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
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
            print(f"Username: {user_data.get('username', 'Не указан')}")
            print(f"Текущая страница: {user_data.get('current_page', 1)}")
            
            # Показываем время создания
            created_at = user_data.get('created_at')
            if created_at:
                print(f"Создан: {created_at.strftime('%d.%m.%Y %H:%M:%S')}")
            
            # Показываем ответы на вопросы
            if user_data.get('question_1') or user_data.get('question_2'):
                print("Ответы на вопросы:")
                print(f"  Вопрос 1 (Возраст): {user_data.get('question_1', 'Не указан')}")
                print(f"  Вопрос 2 (Род деятельности): {user_data.get('question_2', 'Не указан')}")
                print(f"  Вопрос 3 (Доход): {user_data.get('question_3', 'Не указан')}")
                print(f"  Вопрос 4 (Мотивация): {user_data.get('question_4', 'Не указан')}")
                print(f"  Вопрос 5 (Работа в команде): {user_data.get('question_5', 'Не указан')}")
            else:
                print("Ответы на вопросы: Не заполнены")
            
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
        
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            user_data = dict(result)
            print(f"Найден пользователь: {username}")
            print("=" * 50)
            print(f"Текущая страница: {user_data.get('current_page', 1)}")
            
            # Показываем время создания
            created_at = user_data.get('created_at')
            if created_at:
                print(f"Создан: {created_at.strftime('%d.%m.%Y %H:%M:%S')}")
            
            # Показываем ответы на вопросы
            if user_data.get('question_1') or user_data.get('question_2'):
                print("Ответы на вопросы:")
                print(f"  Вопрос 1 (Возраст): {user_data.get('question_1', 'Не указан')}")
                print(f"  Вопрос 2 (Род деятельности): {user_data.get('question_2', 'Не указан')}")
                print(f"  Вопрос 3 (Доход): {user_data.get('question_3', 'Не указан')}")
                print(f"  Вопрос 4 (Мотивация): {user_data.get('question_4', 'Не указан')}")
                print(f"  Вопрос 5 (Работа в команде): {user_data.get('question_5', 'Не указан')}")
            else:
                print("Ответы на вопросы: Не заполнены")
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
        cursor.execute('SELECT COUNT(*) FROM users WHERE question_1 IS NOT NULL OR question_2 IS NOT NULL')
        users_with_forms = cursor.fetchone()[0]
        
        # Последние 5 пользователей
        cursor.execute('SELECT username, current_page, created_at FROM users ORDER BY created_at DESC LIMIT 5')
        recent_users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        print("=== Статистика базы данных ===")
        print(f"Всего пользователей: {total_users}")
        print(f"Пользователей с формами: {users_with_forms}")
        print(f"Пользователей без форм: {total_users - users_with_forms}")
        print("\nПоследние 5 пользователей:")
        for user in recent_users:
            print(f"  {user[0]} - страница {user[1]} - {user[2].strftime('%d.%m.%Y %H:%M:%S')}")
            
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