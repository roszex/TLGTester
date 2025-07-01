#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import psycopg2
from datetime import datetime

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

def get_owners():
    """Читает список владельцев из файла"""
    owners = []
    try:
        with open('owners.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and line.isdigit():
                    owners.append(int(line))
    except FileNotFoundError:
        print("Файл owners.txt не найден!")
    return owners

def get_lead_data(lead_id):
    """Получает данные лида из PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, question_1, question_2, question_3, question_4, question_5, current_page
            FROM users 
            WHERE id = %s
        """, (lead_id,))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            return {
                'user_id': result[0],
                'question_1': result[1],
                'question_2': result[2], 
                'question_3': result[3],
                'question_4': result[4],
                'question_5': result[5],
                'current_page': result[6]
            }
    except Exception as e:
        print(f"Ошибка при получении данных из БД: {e}")
    return None

def send_telegram_message(chat_id, message):
    """Отправляет сообщение в Telegram"""
    if not BOT_TOKEN:
        print("BOT_TOKEN не установлен!")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return True
        else:
            print(f"Ошибка отправки: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        return False

def format_lead_message(lead_data):
    """Форматирует сообщение о лиде"""
    message = f"""🔥 <b>НОВЫЙ ЛИД #{lead_data.get('id', 'N/A')}</b>

👤 <b>ЮЗ:</b> {lead_data.get('user_id', 'N/A')}

❓ <b>Вопрос 1:</b> {lead_data.get('question_1', 'N/A')}

❓ <b>Вопрос 2:</b> {lead_data.get('question_2', 'N/A')}

❓ <b>Вопрос 3:</b> {lead_data.get('question_3', 'N/A')}

❓ <b>Вопрос 4:</b> {lead_data.get('question_4', 'N/A')}

❓ <b>Вопрос 5:</b> {lead_data.get('question_5', 'N/A')}

📅 <b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"""
    
    return message

def notify_owners(lead_id):
    """Отправляет уведомления всем владельцам"""
    owners = get_owners()
    if not owners:
        print("Список владельцев пуст!")
        return
    
    lead_data = get_lead_data(lead_id)
    if not lead_data:
        print(f"Данные лида {lead_id} не найдены!")
        return
    
    lead_data['id'] = lead_id
    message = format_lead_message(lead_data)
    
    success_count = 0
    for owner_id in owners:
        if send_telegram_message(owner_id, message):
            success_count += 1
            print(f"Уведомление отправлено владельцу {owner_id}")
        else:
            print(f"Ошибка отправки владельцу {owner_id}")
    
    print(f"Отправлено {success_count} из {len(owners)} уведомлений")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python send_notification.py <lead_id>")
        sys.exit(1)
    
    lead_id = int(sys.argv[1])
    notify_owners(lead_id) 