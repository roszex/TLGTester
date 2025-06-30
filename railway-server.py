#!/usr/bin/env python3
"""
Простая версия сервера для Railway без базы данных
"""

import os
import json
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Простое хранилище в памяти (для тестирования)
users_data = {}

@app.after_request
def after_request(response):
    """Добавляет CORS заголовки"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def get_or_create_user(user_id):
    """Получает или создает пользователя"""
    if user_id not in users_data:
        users_data[user_id] = {
            'username': user_id,
            'current_page': 1,
            'form_data': None,
            'created_at': '30.06.2024 20:30:00'
        }
        logger.info(f"Created new user: {user_id}")
    return users_data[user_id]

def update_user_progress(user_id, current_page, form_data=None):
    """Обновляет прогресс пользователя"""
    if user_id in users_data:
        users_data[user_id]['current_page'] = current_page
        if form_data:
            users_data[user_id]['form_data'] = form_data
        logger.info(f"Updated progress for user {user_id}: page {current_page}")
        return True
    return False

def get_user_data(user_id):
    """Получает данные пользователя"""
    return users_data.get(user_id)

def get_all_users():
    """Получает всех пользователей"""
    return users_data

# API Routes
@app.route('/api/users', methods=['GET'])
def get_all_users_api():
    """Получает всех пользователей"""
    return jsonify(users_data)

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_data_api(user_id):
    """Получает данные пользователя"""
    user_data = get_user_data(user_id)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

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
    return jsonify({"status": "healthy", "message": "Server is running (simple mode)"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8001))
    print(f"Starting simple server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 