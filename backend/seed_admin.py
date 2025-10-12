from models import SessionLocal, create_tables, User
import bcrypt
create_tables()
db = SessionLocal()
email='admin@estateiq.local'
existing = db.query(User).filter(User.email==email).first()
if existing:
    print('Admin exists')
else:
    pw = 'admin123'
    pw_hash = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    admin = User(name='Admin', email=email, password_hash=pw_hash, role='admin')
    db.add(admin)
    db.commit()
    print('Admin created:', email, pw)
