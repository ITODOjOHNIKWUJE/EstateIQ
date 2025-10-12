from models import SessionLocal, create_tables, User, Property, Unit, Lease, Payment
import bcrypt
create_tables()
db = SessionLocal()
# create demo landlord
land_email = 'landlord@example.com'
land = db.query(User).filter(User.email==land_email).first()
if not land:
    pw = 'landlord123'
    pw_hash = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    land = User(name='Demo Landlord', email=land_email, password_hash=pw_hash, role='landlord')
    db.add(land)
    db.commit()
# create tenant
t1_email='tenant1@example.com'
t1 = db.query(User).filter(User.email==t1_email).first()
if not t1:
    pw='tenant123'
    pw_hash = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    t1 = User(name='Tenant One', email=t1_email, password_hash=pw_hash, role='tenant')
    db.add(t1)
    db.commit()
# create property
prop = db.query(Property).filter(Property.title=='Sunrise Apartments').first()
if not prop:
    prop = Property(owner_id=land.id, title='Sunrise Apartments', address='12 Lagos St', description='Demo property')
    db.add(prop)
    db.commit()
# create unit
u = db.query(Unit).filter(Unit.unit_number=='1A').first()
if not u:
    u = Unit(property_id=prop.id, unit_number='1A', rent_amount=50000, status='occupied')
    db.add(u)
    db.commit()
# lease and payment
lease = Lease(unit_id=u.id, tenant_id=t1.id, rent_amount=50000, start_date='2025-01-01', end_date='2025-12-31')
db.add(lease)
db.commit()
payment = Payment(tenant_id=t1.id, unit_id=u.id, amount=50000, status='paid', method='manual', tx_ref='DEMO-001')
db.add(payment)
db.commit()
print('Demo data created. Landlord:', land.email, 'Tenant:', t1.email)
