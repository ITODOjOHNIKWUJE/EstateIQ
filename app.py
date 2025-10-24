# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allows your React app to communicate

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------
# INITIAL DATABASE SETUP
# -------------------------------
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB at import so Render always has it
init_db()

# -------------------------------
# ROUTES
# -------------------------------
@app.route('/')
def index():
    return jsonify({'status': 'EstateIQ Backend Running'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    conn = get_db_connection()
    existing = conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()

    if existing:
        conn.close()
        return jsonify({'error': 'User already exists'}), 400

    conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE email=? AND password=?',
        (email, password)
    ).fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful', 'token': 'demo_token_123'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# -------------------------------
# PROPERTY ROUTE (FIXED)
# -------------------------------
@app.route('/api/properties', methods=['GET'])
def get_properties():
    properties = [
        {"id": 1, "name": "Ocean View Apartment", "price": 1200, "status": "Available"},
        {"id": 2, "name": "City Center Office", "price": 2500, "status": "Rented"},
        {"id": 3, "name": "Sunset Villa", "price": 3000, "status": "Available"}
    ]
    return jsonify(properties)

# -------------------------------
# RUN APP (local testing only)
# -------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
