from flask import request, jsonify
from models import SessionLocal, Property, Unit

def init_property_routes(app):
    @app.route('/api/properties', methods=['GET'])
    def list_properties():
        db = SessionLocal()
        props = db.query(Property).all()
        out = []
        for p in props:
            units = db.query(Unit).filter(Unit.property_id == p.id).all()
            out.append({'id': p.id, 'title': p.title, 'address': p.address, 'units': [{'id':u.id,'unit_number':u.unit_number,'rent_amount':u.rent_amount,'status':u.status} for u in units]})
        return jsonify(out)

    @app.route('/api/properties', methods=['POST'])
    def create_property():
        data = request.get_json() or {}
        title = data.get('title')
        address = data.get('address')
        description = data.get('description')
        owner_id = data.get('owner_id')
        if not (title and owner_id):
            return jsonify({'error': 'Missing fields'}), 400
        db = SessionLocal()
        prop = Property(title=title, address=address, description=description, owner_id=owner_id)
        db.add(prop)
        db.commit()
        return jsonify({'id': prop.id, 'title': prop.title}), 201

    @app.route('/api/properties/<int:pid>/units', methods=['POST'])
    def create_unit(pid):
        data = request.get_json() or {}
        unit_number = data.get('unit_number')
        rent_amount = data.get('rent_amount')
        status = data.get('status', 'vacant')
        if not unit_number:
            return jsonify({'error': 'Missing fields'}), 400
        db = SessionLocal()
        unit = Unit(property_id=pid, unit_number=unit_number, rent_amount=rent_amount, status=status)
        db.add(unit)
        db.commit()
        return jsonify({'id': unit.id, 'unit_number': unit.unit_number}), 201
