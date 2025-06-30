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
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

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
        
        # Создаем таблицу пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE,
                question_1 TEXT,
                question_2 TEXT,
                question_3 TEXT,
                question_4 TEXT,
                question_5 TEXT,
                current_page INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                INSERT INTO users (username, current_page, created_at)
                VALUES (%s, 1, CURRENT_TIMESTAMP)
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
                'form_data': form_data,
                'created_at': user_data['created_at'].strftime("%d.%m.%Y %H:%M:%S") if user_data['created_at'] else None
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
        
        # Проверяем, есть ли колонка created_at
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'created_at'
        """)
        has_created_at = cursor.fetchone() is not None
        
        if has_created_at:
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        else:
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
            
            # Обрабатываем created_at
            created_at = None
            if has_created_at and user_data.get('created_at'):
                if isinstance(user_data['created_at'], str):
                    created_at = user_data['created_at']
                else:
                    created_at = user_data['created_at'].strftime("%d.%m.%Y %H:%M:%S")
            else:
                created_at = "30.06.2024 20:30:00"  # Fallback
            
            users[user_id] = {
                'username': user_data['username'],
                'current_page': user_data['current_page'],
                'form_data': form_data,
                'created_at': created_at
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