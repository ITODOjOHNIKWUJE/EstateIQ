# backend/routes/leases.py
from flask import request, jsonify
from models import SessionLocal, Lease, Unit, User
from datetime import datetime

def init_lease_routes(app):
    @app.route('/api/leases', methods=['GET'])
    def list_leases():
        db = SessionLocal()
        try:
            leases = db.query(Lease).all()
            out = []
            for l in leases:
                out.append({
                    'id': l.id,
                    'unit_id': l.unit_id,
                    'tenant_id': l.tenant_id,
                    'rent_amount': l.rent_amount,
                    'start_date': l.start_date,
                    'end_date': l.end_date
                })
            return jsonify(out)
        finally:
            db.close()

    @app.route('/api/leases', methods=['POST'])
    def create_lease():
        data = request.get_json() or {}
        unit_id = data.get('unit_id')
        tenant_id = data.get('tenant_id')
        rent_amount = data.get('rent_amount')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if not (unit_id and tenant_id and rent_amount and start_date and end_date):
            return jsonify({'error': 'Missing fields'}), 400
        db = SessionLocal()
        try:
            # optional: validate unit and tenant exist
            unit = db.query(Unit).filter(Unit.id == unit_id).first()
            tenant = db.query(User).filter(User.id == tenant_id).first()
            if not unit or not tenant:
                return jsonify({'error': 'Invalid unit or tenant'}), 400
            lease = Lease(unit_id=unit_id, tenant_id=tenant_id, rent_amount=rent_amount, start_date=start_date, end_date=end_date)
            db.add(lease)
            db.commit()
            db.refresh(lease)
            # mark unit occupied
            unit.status = 'occupied'
            db.commit()
            return jsonify({'id': lease.id}), 201
        finally:
            db.close()
