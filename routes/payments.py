# backend/routes/payments.py
from flask import request, jsonify
from models import SessionLocal, Payment
from routes.auth import token_required

def init_payment_routes(app):
    @app.route('/api/payments', methods=['GET'])
    @token_required
    def list_payments():
        db = SessionLocal()
        try:
            pays = db.query(Payment).all()
            return jsonify([{
                'id': p.id,
                'tenant_id': p.tenant_id,
                'unit_id': p.unit_id,
                'amount': p.amount,
                'status': p.status,
                'method': p.method,
                'tx_ref': p.tx_ref,
                'created_at': p.created_at.isoformat() if p.created_at else None
            } for p in pays])
        finally:
            db.close()

    @app.route('/api/payments', methods=['POST'])
    @token_required
    def create_payment():
        data = request.get_json() or {}
        tenant_id = data.get('tenant_id')
        unit_id = data.get('unit_id')
        amount = data.get('amount')
        method = data.get('method', 'manual')
        tx_ref = data.get('tx_ref', None)
        if not (tenant_id and unit_id and amount):
            return jsonify({'error': 'Missing fields'}), 400
        db = SessionLocal()
        try:
            p = Payment(tenant_id=tenant_id, unit_id=unit_id, amount=amount, method=method, tx_ref=tx_ref, status='paid')
            db.add(p)
            db.commit()
            return jsonify({'id': p.id, 'status': p.status}), 201
        finally:
            db.close()
