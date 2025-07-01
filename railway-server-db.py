#!/usr/bin/env python3
"""
Простая версия сервера для Railway с PostgreSQL базой данных
Версия: 2.0 - с базой данных
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import threading
import requests
import subprocess

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Настройка кодировки для русского языка
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def get_owners():
    """Читает список владельцев из JSON файла"""
    import json
    owners = []
    try:
        with open('owners.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            owners = data.get('owners', [])
            logger.info(f"Загружено {len(owners)} владельцев из owners.json")
    except FileNotFoundError:
        logger.warning("Файл owners.json не найден!")
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга owners.json: {e}")
    except Exception as e:
        logger.error(f"Ошибка чтения owners.json: {e}")
    return owners

def send_telegram_message(chat_id, message):
    """Отправляет сообщение в Telegram"""
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logger.error("BOT_TOKEN не установлен!")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
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
            logger.error(f"Ошибка отправки: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        return False

def format_lead_message(lead_data):
    """Форматирует сообщение о лиде"""
    message = f"""🔥 <b>НОВЫЙ ЛИД #{lead_data.get('id', 'N/A')}</b>

👤 <b>ЮЗ:</b> {lead_data.get('user_id', 'N/A')}

❓ <b>Вопрос 1:</b> {lead_data.get('question_1', 'N/A')}

❓ <b>Вопрос 2:</b> {lead_data.get('question_2', 'N/A')}

❓ <b>Вопрос 3:</b> {lead_data.get('question_3', 'N/A')}

❓ <b>Вопрос 4:</b> {lead_data.get('question_4', 'N/A')}

❓ <b>Вопрос 5:</b> {lead_data.get('question_5', 'N/A')}"""
    
    return message

def notify_owners_async(lead_id, user_id, form_data):
    """Асинхронно отправляет уведомления владельцам"""
    def send_notifications():
        try:
            owners = get_owners()
            if not owners:
                logger.warning("Список владельцев пуст!")
                return
            
            # Формируем данные лида
            lead_data = {
                'id': lead_id,
                'user_id': user_id,
                'question_1': form_data.get('age', 'N/A'),
                'question_2': form_data.get('occupation', 'N/A'),
                'question_3': form_data.get('income', 'N/A'),
                'question_4': form_data.get('motivation', 'N/A'),
                'question_5': form_data.get('teamwork', 'N/A')
            }
            
            message = format_lead_message(lead_data)
            
            success_count = 0
            for owner_id in owners:
                if send_telegram_message(owner_id, message):
                    success_count += 1
                    logger.info(f"Уведомление отправлено владельцу {owner_id}")
                else:
                    logger.error(f"Ошибка отправки владельцу {owner_id}")
            
            logger.info(f"Отправлено {success_count} из {len(owners)} уведомлений")
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомлений: {e}")
    
    # Запускаем в отдельном потоке
    thread = threading.Thread(target=send_notifications)
    thread.daemon = True
    thread.start()

def get_db_connection():
    """Получает соединение с базой данных PostgreSQL"""
    try:
        # Получаем DATABASE_URL от Railway
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            logger.info("Connecting to Railway PostgreSQL database")
            conn = psycopg2.connect(database_url)
            logger.info("Successfully connected to Railway database")
            return conn
        else:
            logger.error("DATABASE_URL not found")
            return None
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def init_database():
    """Инициализирует базу данных и создает таблицы"""
    conn = get_db_connection()
    if not conn:
        logger.error("Cannot connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Создаем таблицу пользователей без created_at
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE,
                question_1 TEXT,
                question_2 TEXT,
                question_3 TEXT,
                question_4 TEXT,
                question_5 TEXT,
                current_page INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        return False

def get_or_create_user(user_id):
    """Получает или создает пользователя в базе данных"""
    logger.info(f"Getting or creating user: {user_id}")
    conn = get_db_connection()
    if not conn:
        logger.error("Failed to get database connection")
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Проверяем, существует ли пользователь
        cursor.execute('SELECT * FROM users WHERE username = %s', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            # Создаем нового пользователя
            cursor.execute('''
                INSERT INTO users (username, current_page)
                VALUES (%s, 1)
                RETURNING *
            ''', (user_id,))
            user = cursor.fetchone()
            logger.info(f"Successfully created new user: {user_id}")
        else:
            logger.info(f"User already exists: {user_id}")
        
        conn.commit()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        logger.error(f"Error getting/creating user {user_id}: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None

def update_user_progress(user_id, current_page, form_data=None):
    """Обновляет прогресс пользователя в базе данных"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Обновляем текущую страницу
        cursor.execute('''
            UPDATE users 
            SET current_page = %s
            WHERE username = %s
        ''', (current_page, user_id))
        
        # Если есть данные формы, сохраняем их
        if form_data:
            cursor.execute('''
                UPDATE users 
                SET question_1 = %s, question_2 = %s, question_3 = %s, question_4 = %s, question_5 = %s
                WHERE username = %s
            ''', (
                form_data.get('age'),
                form_data.get('occupation'),
                form_data.get('income'),
                form_data.get('motivation'),
                form_data.get('teamwork'),
                user_id
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Updated progress for user {user_id}: page {current_page}")
        return True
    except Exception as e:
        logger.error(f"Error updating user progress: {e}")
        return False

def get_user_data(user_id):
    """Получает данные пользователя из базы данных"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('SELECT * FROM users WHERE username = %s', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            user_data = dict(result)
            
            # Формируем form_data в нужном формате
            form_data = None
            if user_data.get('question_1') or user_data.get('question_2'):
                form_data = {
                    'age': user_data.get('question_1'),
                    'occupation': user_data.get('question_2'),
                    'income': user_data.get('question_3'),
                    'motivation': user_data.get('question_4'),
                    'teamwork': user_data.get('question_5')
                }
            
            return {
                'user_id': user_data['username'],
                'username': user_data['username'],
                'current_page': user_data['current_page'],
                'form_data': form_data
            }
        
        return None
    except Exception as e:
        logger.error(f"Error getting user data: {e}")
        return None

def get_all_users():
    """Получает всех пользователей из базы данных"""
    conn = get_db_connection()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Получаем всех пользователей, сортируем по ID
        cursor.execute('SELECT * FROM users ORDER BY id DESC')
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        users = {}
        for row in results:
            user_data = dict(row)
            user_id = user_data['username']
            
            # Формируем form_data в нужном формате
            form_data = None
            if user_data.get('question_1') or user_data.get('question_2'):
                form_data = {
                    'age': user_data.get('question_1'),
                    'occupation': user_data.get('question_2'),
                    'income': user_data.get('question_3'),
                    'motivation': user_data.get('question_4'),
                    'teamwork': user_data.get('question_5')
                }
            
            users[user_id] = {
                'username': user_data['username'],
                'current_page': user_data['current_page'],
                'form_data': form_data
            }
        
        return users
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return {}

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "Server is running with PostgreSQL database"})

@app.route('/api/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify(users)

@app.route('/api/save_form_data', methods=['POST'])
def save_form_data():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        form_data = data.get('form_data')
        
        if not user_id or not form_data:
            return jsonify({'error': 'Missing data'}), 400
        
        # Получаем или создаем пользователя
        user = get_or_create_user(user_id)
        if not user:
            return jsonify({'error': 'Failed to create user'}), 500
        
        # Обновляем данные формы (сохраняем текущую страницу как 4)
        success = update_user_progress(user_id, 4, form_data)
        
        if success:
            notify_owners_async(user['id'], user['username'], form_data)
            return jsonify({
                'message': 'Form data saved successfully', 
                'user_id': user_id,
                'form_data': form_data
            })
        else:
            return jsonify({'error': 'Failed to save form data'}), 500
            
    except Exception as e:
        logger.error(f"Error in save_form_data: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        current_page = data.get('current_page', 1)
        
        if not user_id:
            return jsonify({'error': 'Missing user_id'}), 400
        
        # Получаем или создаем пользователя
        user = get_or_create_user(user_id)
        if not user:
            return jsonify({'error': 'Failed to create user'}), 500
        
        # Обновляем прогресс
        success = update_user_progress(user_id, current_page)
        
        if success:
            return jsonify({
                'message': 'Progress saved successfully', 
                'user_id': user_id, 
                'current_page': current_page
            })
        else:
            return jsonify({'error': 'Failed to save progress'}), 500
            
    except Exception as e:
        logger.error(f"Error in save_progress: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/get_progress/<user_id>', methods=['GET'])
def get_progress(user_id):
    user_data = get_user_data(user_id)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/')
def index():
    return send_from_directory('webapp', 'page_1/index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('webapp', filename)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8001))
    print(f"Starting server on port {port}")
    
    # Инициализируем базу данных
    if init_database():
        print("Database initialized successfully")
    else:
        print("Failed to initialize database")
    
    app.run(host='0.0.0.0', port=port, debug=False) 