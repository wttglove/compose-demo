from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'running',
        'message': 'Hello from Docker Compose API! 🐳',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'container': 'api-service'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
