# backend/routes/auth.py
from flask import request, jsonify, current_app, g
from functools import wraps
import jwt
from datetime import datetime, timedelta
from models import SessionLocal, User
import bcrypt

def init_auth_routes(app):
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        data = request.get_json() or {}
        data = request.get_json() or {}
        print("🔍 Login data received:", data)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'tenant')
        if not (name and email and password):
            return jsonify({'error': 'Missing fields'}), 400
        db = SessionLocal()
        try:
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                return jsonify({'error': 'Email exists'}), 400
            pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User(name=name, email=email, password_hash=pw_hash, role=role)
            db.add(user)
            db.commit()
            return jsonify({'message': 'registered', 'user': {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}}), 201
        finally:
            db.close()

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        if not (email and password):
            return jsonify({'error': 'Missing fields'}), 400
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return jsonify({'error': 'Invalid credentials'}), 401
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                payload = {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(hours=8)
                }
                token = jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
                return jsonify({'access_token': token, 'user': {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}}), 200
            return jsonify({'error': 'Invalid credentials'}), 401
        finally:
            db.close()

# token_required decorator to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Authorization: Bearer <token>
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            user_id = data.get('user_id')
            db = SessionLocal()
            g.current_user = db.query(User).get(user_id)
            db.close()
            if g.current_user is None:
                return jsonify({'error': 'Invalid token user'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except Exception as e:
            return jsonify({'error': 'Token invalid', 'detail': str(e)}), 401
        return f(*args, **kwargs)
    return decorated
