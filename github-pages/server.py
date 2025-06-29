from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from env.github
load_dotenv('env.github')

app = Flask(__name__)

# Улучшенные CORS настройки для мобильных устройств и Telegram WebApp
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "X-Telegram-WebApp", "X-User-ID"],
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

# Добавляем middleware для обработки CORS preflight запросов
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

def log_request_info(request, user_id):
    """Логирует информацию о запросе для диагностики"""
    print(f"[{get_readable_datetime()}] Request: {request.method} {request.path}")
    print(f"  User ID: {user_id}")
    print(f"  Origin: {request.headers.get('Origin', 'Unknown')}")
    print(f"  User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    print(f"  X-Telegram-WebApp: {request.headers.get('X-Telegram-WebApp', 'No')}")
    print(f"  X-User-ID: {request.headers.get('X-User-ID', 'No')}")
    if request.is_json:
        print(f"  JSON Data: {request.get_json()}")

PORT = int(os.getenv('PORT', 8001))

# API Routes for user data
@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_data(user_id):
    """Получает данные пользователя"""
    log_request_info(request, user_id)
    user_data = get_or_create_user(user_id)
    print(f"  Response: {user_data}")
    return jsonify(user_data)

@app.route('/api/user/<user_id>', methods=['POST'])
def update_user_data(user_id):
    """Обновляет данные пользователя"""
    log_request_info(request, user_id)
    data = request.get_json()
    user_data = load_user_data()
    
    if user_id not in user_data:
        user_data[user_id] = {
            'username': None,
            'form_data': None,
            'current_page': 1,
            'created_at': get_readable_datetime()
        }
    
    # Обновляем только переданные поля
    if 'username' in data:
        user_data[user_id]['username'] = data['username']
    if 'form_data' in data:
        # Убираем timestamp и userAgent из данных формы
        form_data = data['form_data'].copy()
        if 'timestamp' in form_data:
            del form_data['timestamp']
        if 'userAgent' in form_data:
            del form_data['userAgent']
        user_data[user_id]['form_data'] = form_data
    if 'current_page' in data:
        user_data[user_id]['current_page'] = data['current_page']
    
    save_user_data(user_data)
    print(f"  Updated user data: {user_data[user_id]}")
    return jsonify({'status': 'success', 'message': 'User data updated'})

@app.route('/api/progress/<user_id>', methods=['GET'])
def get_progress(user_id):
    """Получает прогресс пользователя (для обратной совместимости)"""
    log_request_info(request, user_id)
    user_data = get_or_create_user(user_id)
    response_data = {
        'user_id': user_id,
        'current_page': user_data['current_page']
    }
    print(f"  Response: {response_data}")
    return jsonify(response_data)

@app.route('/api/progress/<user_id>', methods=['POST'])
def update_progress(user_id):
    """Обновляет прогресс пользователя (для обратной совместимости)"""
    log_request_info(request, user_id)
    data = request.get_json()
    page = data.get('page', 1)
    
    user_data = load_user_data()
    if user_id not in user_data:
        user_data[user_id] = {
            'username': None,
            'form_data': None,
            'current_page': page,
            'created_at': get_readable_datetime()
        }
    else:
        user_data[user_id]['current_page'] = page
    
    save_user_data(user_data)
    print(f"  Updated progress to page {page}")
    return jsonify({'status': 'success', 'message': f'Progress updated to page {page}'})

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    """Новый endpoint для сохранения прогресса"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    log_request_info(request, user_id)
    
    user_data = load_user_data()
    if user_id not in user_data:
        user_data[user_id] = {
            'username': None,
            'form_data': None,
            'current_page': 1,
            'created_at': get_readable_datetime()
        }
    
    # Обновляем текущую страницу
    if 'current_page' in data:
        user_data[user_id]['current_page'] = data['current_page']
    
    # Обновляем данные формы если есть
    if 'form_data' in data:
        form_data = data['form_data'].copy()
        if 'timestamp' in form_data:
            del form_data['timestamp']
        if 'userAgent' in form_data:
            del form_data['userAgent']
        user_data[user_id]['form_data'] = form_data
    
    save_user_data(user_data)
    print(f"  Saved progress: {user_data[user_id]}")
    return jsonify({'status': 'success', 'message': 'Progress saved'})

@app.route('/api/get_progress/<user_id>', methods=['GET'])
def get_progress_new(user_id):
    """Новый endpoint для получения прогресса"""
    log_request_info(request, user_id)
    user_data = get_or_create_user(user_id)
    
    response_data = {
        'user_id': user_id,
        'current_page': user_data['current_page'],
        'form_data': user_data.get('form_data'),
        'username': user_data.get('username')
    }
    print(f"  Response: {response_data}")
    return jsonify(response_data)

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Получает всех пользователей (для админа)"""
    data = load_user_data()
    return jsonify(data)

# Static file serving
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('webapp', filename)

@app.route('/')
def index():
    return send_from_directory('webapp', 'page_1/index.html')

@app.route('/page_<int:page_num>/<path:filename>')
def serve_page(page_num, filename):
    return send_from_directory(f'webapp/page_{page_num}', filename)

if __name__ == '__main__':
    print(f"Starting server on port {PORT}")
    print(f"User data file: {USER_DATA_FILE}")
    app.run(host='0.0.0.0', port=PORT, debug=True) 