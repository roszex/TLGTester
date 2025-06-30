from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS settings
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "X-Telegram-WebApp", "X-User-ID"],
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,X-Telegram-WebApp,X-User-ID')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Database connection
def get_db_connection():
    """Получает соединение с базой данных"""
    try:
        # Получаем переменные окружения от Railway
        database_url = os.getenv('DATABASE_URL')
        logger.info(f"Database URL available: {bool(database_url)}")
        
        if database_url:
            # Railway предоставляет DATABASE_URL в формате postgresql://user:pass@host:port/db
            logger.info("Connecting to Railway PostgreSQL database")
            conn = psycopg2.connect(database_url)
            logger.info("Successfully connected to Railway database")
        else:
            # Fallback для локальной разработки
            logger.info("Using local database connection")
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'emelyanov_bot'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', ''),
                port=os.getenv('DB_PORT', '5432')
            )
            logger.info("Successfully connected to local database")
        
        return conn
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
        
        # Создаем таблицу пользователей с новой структурой
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100),
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
        logger.info(f"Checking if user exists: {user_id}")
        cursor.execute('SELECT * FROM users WHERE username = %s', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            # Создаем нового пользователя
            logger.info(f"Creating new user: {user_id}")
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
    """Обновляет прогресс пользователя"""
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
    """Получает полные данные пользователя"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Получаем данные пользователя
        cursor.execute('SELECT * FROM users WHERE username = %s', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            # Преобразуем в словарь
            user_data = dict(result)
            
            # Формируем form_data в старом формате для совместимости
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
    """Получает всех пользователей"""
    conn = get_db_connection()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        users = {}
        for row in results:
            user_data = dict(row)
            user_id = user_data['username']
            
            # Формируем form_data в старом формате для совместимости
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
                'form_data': form_data,
                'created_at': user_data['created_at'].strftime("%d.%m.%Y %H:%M:%S") if user_data['created_at'] else None
            }
        
        return users
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return {}

# API Routes
@app.route('/api/users', methods=['GET'])
def get_all_users_api():
    """Получает всех пользователей"""
    users = get_all_users()
    return jsonify(users)

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_data_api(user_id):
    """Получает данные пользователя"""
    user_data = get_user_data(user_id)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/user/<user_id>', methods=['POST'])
def update_user_data_api(user_id):
    """Обновляет данные пользователя"""
    data = request.get_json()
    
    # Получаем или создаем пользователя
    user = get_or_create_user(user_id)
    if not user:
        return jsonify({'error': 'Failed to create user'}), 500
    
    # Обновляем прогресс
    current_page = data.get('current_page', 1)
    form_data = data.get('form_data')
    
    if update_user_progress(user_id, current_page, form_data):
        return jsonify({'status': 'success', 'message': 'User data updated'})
    else:
        return jsonify({'error': 'Failed to update user data'}), 500

@app.route('/api/save_progress', methods=['POST'])
def save_progress_api():
    """Сохраняет прогресс пользователя"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        current_page = data.get('current_page', 1)
        form_data = data.get('form_data')
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        # Получаем или создаем пользователя
        user = get_or_create_user(user_id)
        if not user:
            return jsonify({'error': 'Failed to create user'}), 500
        
        # Обновляем прогресс
        success = update_user_progress(user_id, current_page, form_data)
        
        if success:
            return jsonify({'message': 'Progress saved successfully', 'user_id': user_id, 'current_page': current_page})
        else:
            return jsonify({'error': 'Failed to save progress'}), 500
            
    except Exception as e:
        logger.error(f"Error in save_progress_api: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/save_form_data', methods=['POST'])
def save_form_data_api():
    """Сохраняет данные формы пользователя"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        form_data = data.get('form_data')
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        if not form_data:
            return jsonify({'error': 'form_data is required'}), 400
        
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
        logger.error(f"Error in save_form_data_api: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/get_progress/<user_id>', methods=['GET'])
def get_progress_api(user_id):
    """Получает прогресс"""
    user_data = get_user_data(user_id)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

# Static file serving for WebApp
@app.route('/')
def index():
    return send_from_directory('webapp', 'page_1/index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Раздает статические файлы из папки webapp"""
    return send_from_directory('webapp', filename)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "Server is running with database"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8001))
    print(f"Starting server on port {port}")
    
    # Инициализируем базу данных
    if init_database():
        print("Database initialized successfully")
    else:
        print("Failed to initialize database")
    
    app.run(host='0.0.0.0', port=port, debug=False) 