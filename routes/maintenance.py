from flask import request, jsonify
from models import SessionLocal, MaintenanceTicket

def init_maintenance_routes(app):
    @app.route('/api/maintenance', methods=['POST'])
    def create_ticket():
        data = request.get_json() or {}
        tenant_id = data.get('tenant_id')
        unit_id = data.get('unit_id')
        title = data.get('title')
        description = data.get('description')
        if not (tenant_id and unit_id and title):
            return jsonify({'error': 'Missing fields'}), 400
        db = SessionLocal()
        t = MaintenanceTicket(tenant_id=tenant_id, unit_id=unit_id, title=title, description=description)
        db.add(t)
        db.commit()
        return jsonify({'id': t.id, 'status': t.status}), 201

    @app.route('/api/maintenance', methods=['GET'])
    def list_tickets():
        db = SessionLocal()
        ts = db.query(MaintenanceTicket).all()
        return jsonify([{'id':t.id,'title':t.title,'status':t.status,'unit_id':t.unit_id,'created_at':t.created_at.isoformat()} for t in ts])
