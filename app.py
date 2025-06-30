from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Простое хранилище в памяти
users_data = {}

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "Server is running"})

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users_data)

@app.route('/api/save_form_data', methods=['POST'])
def save_form_data():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        form_data = data.get('form_data')
        
        if not user_id or not form_data:
            return jsonify({'error': 'Missing data'}), 400
        
        users_data[user_id] = {
            'username': user_id,
            'current_page': 4,
            'form_data': form_data,
            'created_at': '30.06.2024 20:30:00'
        }
        
        return jsonify({
            'message': 'Form data saved successfully', 
            'user_id': user_id,
            'form_data': form_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        current_page = data.get('current_page', 1)
        
        if not user_id:
            return jsonify({'error': 'Missing user_id'}), 400
        
        if user_id not in users_data:
            users_data[user_id] = {
                'username': user_id,
                'current_page': current_page,
                'form_data': None,
                'created_at': '30.06.2024 20:30:00'
            }
        else:
            users_data[user_id]['current_page'] = current_page
        
        return jsonify({
            'message': 'Progress saved successfully', 
            'user_id': user_id, 
            'current_page': current_page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('webapp', 'page_1/index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('webapp', filename)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=False) 