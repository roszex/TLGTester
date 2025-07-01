#!/usr/bin/env python3
"""
Скрипт для сброса счётчика ID в базе данных PostgreSQL
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    """Получает соединение с базой данных"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return None

def reset_id_sequence():
    """Сбрасывает счётчик ID до 1"""
    conn = get_db_connection()
    if not conn:
        logger.error("Не удалось подключиться к базе данных")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Получаем текущее количество пользователей
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        logger.info(f"Текущее количество пользователей: {user_count}")
        
        # Сбрасываем счётчик ID до 1
        cursor.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1')
        
        # Если есть пользователи, устанавливаем счётчик на количество пользователей + 1
        if user_count > 0:
            cursor.execute(f'ALTER SEQUENCE users_id_seq RESTART WITH {user_count + 1}')
            logger.info(f"Счётчик ID установлен на {user_count + 1}")
        else:
            logger.info("Счётчик ID установлен на 1 (база данных пуста)")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("✅ Счётчик ID успешно сброшен!")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при сбросе счётчика ID: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def show_current_stats():
    """Показывает текущую статистику базы данных"""
    conn = get_db_connection()
    if not conn:
        logger.error("Не удалось подключиться к базе данных")
        return
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Получаем статистику
        cursor.execute('SELECT COUNT(*) as total FROM users')
        total_users = cursor.fetchone()['total']
        
        cursor.execute('SELECT MAX(id) as max_id FROM users')
        max_id_result = cursor.fetchone()
        max_id = max_id_result['max_id'] if max_id_result['max_id'] else 0
        
        cursor.execute('SELECT MIN(id) as min_id FROM users')
        min_id_result = cursor.fetchone()
        min_id = min_id_result['min_id'] if min_id_result['min_id'] else 0
        
        # Получаем следующий ID из последовательности
        cursor.execute("SELECT nextval('users_id_seq')")
        next_id = cursor.fetchone()[0]
        
        # Возвращаем счётчик на предыдущее значение
        cursor.execute("SELECT setval('users_id_seq', %s, false)", (next_id - 1,))
        
        logger.info("📊 ТЕКУЩАЯ СТАТИСТИКА БАЗЫ ДАННЫХ")
        logger.info("=" * 50)
        logger.info(f"👥 Всего пользователей: {total_users}")
        logger.info(f"🔢 Минимальный ID: {min_id}")
        logger.info(f"🔢 Максимальный ID: {max_id}")
        logger.info(f"🔢 Следующий ID будет: {next_id}")
        
        if total_users > 0:
            logger.info(f"📈 Разрыв между количеством пользователей и максимальным ID: {max_id - total_users}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Ошибка при получении статистики: {e}")
        if conn:
            conn.close()

def optimize_id_sequence():
    """Оптимизирует последовательность ID, чтобы она соответствовала количеству пользователей"""
    conn = get_db_connection()
    if not conn:
        logger.error("Не удалось подключиться к базе данных")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Получаем количество пользователей
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Если база пуста, устанавливаем счётчик на 1
            cursor.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1')
            logger.info("База данных пуста, счётчик установлен на 1")
        else:
            # Если есть пользователи, устанавливаем счётчик на количество + 1
            cursor.execute(f'ALTER SEQUENCE users_id_seq RESTART WITH {user_count + 1}')
            logger.info(f"Счётчик установлен на {user_count + 1} (количество пользователей + 1)")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("✅ Последовательность ID оптимизирована!")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при оптимизации последовательности ID: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def main():
    logger.info("🔄 СБРОС СЧЁТЧИКА ID В БАЗЕ ДАННЫХ")
    logger.info("=" * 50)
    
    if not DATABASE_URL:
        logger.error("❌ DATABASE_URL не установлен в переменных окружения")
        return
    
    # Показываем текущую статистику
    logger.info("📊 ПЕРЕД СБРОСОМ:")
    show_current_stats()
    
    print("\n" + "=" * 50)
    
    # Спрашиваем пользователя
    choice = input("Выберите действие:\n1. Сбросить счётчик ID до 1\n2. Оптимизировать счётчик ID (установить на количество пользователей + 1)\n3. Только показать статистику\n\nВведите номер (1-3): ").strip()
    
    if choice == "1":
        logger.info("🔄 Сбрасываем счётчик ID до 1...")
        if reset_id_sequence():
            logger.info("✅ Сброс завершён!")
        else:
            logger.error("❌ Ошибка при сбросе!")
    
    elif choice == "2":
        logger.info("🔄 Оптимизируем счётчик ID...")
        if optimize_id_sequence():
            logger.info("✅ Оптимизация завершена!")
        else:
            logger.error("❌ Ошибка при оптимизации!")
    
    elif choice == "3":
        logger.info("📊 Показываем только статистику...")
    
    else:
        logger.error("❌ Неверный выбор!")
        return
    
    print("\n" + "=" * 50)
    
    # Показываем статистику после изменений
    logger.info("📊 ПОСЛЕ ИЗМЕНЕНИЙ:")
    show_current_stats()

if __name__ == "__main__":
    main() 