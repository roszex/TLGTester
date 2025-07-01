#!/usr/bin/env python3
"""
Скрипт для управления счётчиком ID через Railway API
"""

import requests
import json

# URL Railway API
RAILWAY_API_URL = 'https://emelyanovtgbot-webapp-production.up.railway.app'

def get_id_stats():
    """Получает статистику ID из API"""
    try:
        response = requests.get(f'{RAILWAY_API_URL}/api/get_id_stats')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")
        return None

def reset_id_counter():
    """Сбрасывает счётчик ID через API"""
    try:
        response = requests.post(f'{RAILWAY_API_URL}/api/reset_id_counter')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка при сбросе счётчика: {e}")
        return None

def show_stats():
    """Показывает статистику ID"""
    stats = get_id_stats()
    if not stats:
        print("❌ Не удалось получить статистику")
        return
    
    print("📊 СТАТИСТИКА ID В БАЗЕ ДАННЫХ")
    print("=" * 50)
    print(f"👥 Всего пользователей: {stats['total_users']}")
    print(f"🔢 Минимальный ID: {stats['min_id']}")
    print(f"🔢 Максимальный ID: {stats['max_id']}")
    print(f"🔢 Следующий ID будет: {stats['next_id']}")
    
    if stats['total_users'] > 0:
        gap = stats['id_gap']
        print(f"📈 Разрыв между количеством пользователей и максимальным ID: {gap}")
        
        if gap > 10:
            print("⚠️  Большой разрыв! Рекомендуется сброс счётчика")
        elif gap > 0:
            print("⚠️  Небольшой разрыв, но можно оптимизировать")
        else:
            print("✅ Счётчик оптимален!")
    else:
        print("✅ База данных пуста, счётчик на 1")

def main():
    print("🔄 УПРАВЛЕНИЕ СЧЁТЧИКОМ ID")
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
    
    # Показываем текущую статистику
    print("\n📊 ТЕКУЩАЯ СТАТИСТИКА:")
    show_stats()
    
    print("\n" + "=" * 50)
    
    # Спрашиваем пользователя
    choice = input("Выберите действие:\n1. Сбросить счётчик ID\n2. Только показать статистику\n\nВведите номер (1-2): ").strip()
    
    if choice == "1":
        print("\n🔄 Сбрасываем счётчик ID...")
        result = reset_id_counter()
        if result:
            print("✅ Счётчик успешно сброшен!")
            print(f"📊 Пользователей: {result['user_count']}")
            print(f"🔢 Следующий ID: {result['next_id']}")
        else:
            print("❌ Ошибка при сбросе счётчика!")
    
    elif choice == "2":
        print("\n📊 Показываем только статистику...")
    
    else:
        print("❌ Неверный выбор!")
        return
    
    print("\n" + "=" * 50)
    
    # Показываем статистику после изменений
    print("📊 ПОСЛЕ ИЗМЕНЕНИЙ:")
    show_stats()
    
    print("\n💡 ВАЖНО:")
    print("   • Счётчик ID автоматически увеличивается при создании пользователей")
    print("   • При удалении пользователей счётчик НЕ сбрасывается")
    print("   • Это нормальное поведение PostgreSQL")
    print("   • Сброс счётчика устанавливает его на количество пользователей + 1")

if __name__ == "__main__":
    main() 