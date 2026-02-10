from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)

# Database connection settings from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'database': os.getenv('DB_NAME', 'devops_db'),
    'user': os.getenv('DB_USER', 'devops_user'),
    'password': os.getenv('DB_PASSWORD', 'devops_pass')
}

def get_db_connection():
    """Create database connection with retry logic"""
    max_retries = 5
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except psycopg2.OperationalError:
            if i < max_retries - 1:
                time.sleep(2)
            else:
                raise

def init_db():
    """Initialize database table"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            endpoint VARCHAR(100)
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Initialize DB on startup
try:
    init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"❌ Database initialization failed: {e}")

@app.route('/api/status')
def status():
    """Get API status and save visit to database"""
    try:
        # Save visit to database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO visits (endpoint) VALUES (%s)", ('/api/status',))
        conn.commit()
        
        # Get total visits count
        cur.execute("SELECT COUNT(*) FROM visits")
        total_visits = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'running',
            'message': 'Hello from Docker Compose API with PostgreSQL! 🐳🐘',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'container': 'api-service',
            'database': 'connected',
            'total_visits': total_visits
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'database': 'disconnected'
        }), 500

@app.route('/api/visits')
def visits():
    """Get all visits from database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, timestamp, endpoint FROM visits ORDER BY timestamp DESC LIMIT 10")
        rows = cur.fetchall()
        
        visits_list = [
            {
                'id': row[0],
                'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
                'endpoint': row[2]
            }
            for row in rows
        ]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'visits': visits_list,
            'count': len(visits_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)