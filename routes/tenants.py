# backend/routes/tenants.py
from flask import request, jsonify
from models import SessionLocal, User

def init_tenant_routes(app):
    @app.route('/api/tenants', methods=['GET'])
    def list_tenants():
        db = SessionLocal()
        try:
            users = db.query(User).filter(User.role == 'tenant').all()
            out = []
            for u in users:
                out.append({
                    'id': u.id,
                    'name': u.name,
                    'email': u.email,
                    'phone': u.phone,
                    'created_at': u.created_at.isoformat() if u.created_at else None
                })
            return jsonify(out)
        finally:
            db.close()

    @app.route('/api/tenants', methods=['POST'])
    def create_tenant():
        data = request.get_json() or {}
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password', 'tenant123')  # default for quick creation; frontend should require password
        if not (name and email):
            return jsonify({'error': 'Missing fields'}), 400
        db = SessionLocal()
        try:
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                return jsonify({'error': 'Email exists'}), 400
            # lightweight hashing (bcrypt already used elsewhere)
            import bcrypt
            pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            tenant = User(name=name, email=email, phone=phone, password_hash=pw_hash, role='tenant')
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            return jsonify({'id': tenant.id, 'name': tenant.name, 'email': tenant.email}), 201
        finally:
            db.close()
