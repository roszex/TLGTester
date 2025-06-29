from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

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

# JSON file for storing user data
USER_DATA_FILE = 'user_data.json'

def load_user_data():
    """Загружает данные пользователей из JSON файла"""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_user_data(data):
    """Сохраняет данные пользователей в JSON файл"""
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_readable_datetime():
    """Возвращает читаемую дату и время"""
    now = datetime.now()
    return now.strftime("%d.%m.%Y %H:%M:%S")

def get_or_create_user(user_id):
    """Получает или создает пользователя в данных"""
    data = load_user_data()
    if user_id not in data:
        data[user_id] = {
            'username': None,
            'form_data': None,
            'current_page': 1,
            'created_at': get_readable_datetime()
        }
        save_user_data(data)
    return data[user_id]

# API Routes
@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Получает всех пользователей"""
    data = load_user_data()
    return jsonify(data)

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_data(user_id):
    """Получает данные пользователя"""
    user_data = get_or_create_user(user_id)
    return jsonify(user_data)

@app.route('/api/user/<user_id>', methods=['POST'])
def update_user_data(user_id):
    """Обновляет данные пользователя"""
    data = request.get_json()
    user_data = load_user_data()
    
    if user_id not in user_data:
        user_data[user_id] = {
            'username': None,
            'form_data': None,
            'current_page': 1,
            'created_at': get_readable_datetime()
        }
    
    if 'username' in data:
        user_data[user_id]['username'] = data['username']
    if 'form_data' in data:
        form_data = data['form_data'].copy()
        if 'timestamp' in form_data:
            del form_data['timestamp']
        if 'userAgent' in form_data:
            del form_data['userAgent']
        user_data[user_id]['form_data'] = form_data
    if 'current_page' in data:
        user_data[user_id]['current_page'] = data['current_page']
    
    save_user_data(user_data)
    return jsonify({'status': 'success', 'message': 'User data updated'})

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    """Сохраняет прогресс"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    user_data = load_user_data()
    if user_id not in user_data:
        user_data[user_id] = {
            'username': None,
            'form_data': None,
            'current_page': 1,
            'created_at': get_readable_datetime()
        }
    
    if 'current_page' in data:
        user_data[user_id]['current_page'] = data['current_page']
    
    if 'form_data' in data:
        form_data = data['form_data'].copy()
        if 'timestamp' in form_data:
            del form_data['timestamp']
        if 'userAgent' in form_data:
            del form_data['userAgent']
        user_data[user_id]['form_data'] = form_data
    
    save_user_data(user_data)
    return jsonify({'status': 'success', 'message': 'Progress saved'})

@app.route('/api/get_progress/<user_id>', methods=['GET'])
def get_progress(user_id):
    """Получает прогресс"""
    user_data = get_or_create_user(user_id)
    
    response_data = {
        'user_id': user_id,
        'current_page': user_data['current_page'],
        'form_data': user_data.get('form_data'),
        'username': user_data.get('username')
    }
    return jsonify(response_data)

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
    return jsonify({"status": "healthy", "message": "Server is running"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8001))
    print(f"Starting server on port {port}")
    print(f"User data file: {USER_DATA_FILE}")
    app.run(host='0.0.0.0', port=port, debug=False) 