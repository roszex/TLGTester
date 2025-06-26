from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from env.local
load_dotenv('env.local')

app = Flask(__name__)
CORS(app)

PORT = int(os.getenv('PORT', 8001))

# Serve static files from the webapp directory
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('webapp', filename)

@app.route('/')
def index():
    return send_from_directory('webapp/page_1', 'index.html')

@app.route('/index.html')
def index_html():
    return send_from_directory('webapp', 'index.html')

@app.route('/page_<int:page_num>/<path:filename>')
def serve_page(page_num, filename):
    return send_from_directory(f'webapp/page_{page_num}', filename)

@app.route('/page_<int:page_num>/')
def serve_page_index(page_num):
    return send_from_directory(f'webapp/page_{page_num}', 'index.html')

# Serve static files from page directories
@app.route('/style.css')
def serve_style():
    return send_from_directory('webapp/page_1', 'style.css')

@app.route('/main.js')
def serve_main_js():
    return send_from_directory('webapp/page_1', 'main.js')

if __name__ == '__main__':
    print(f"Server starting on port {PORT}")
    print(f"WebApp URL: {os.getenv('WEBAPP_URL')}")
    app.run(host='0.0.0.0', port=PORT, debug=True) 