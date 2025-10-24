from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime, os

# Ensure Render can write to the database folder
os.makedirs("instance", exist_ok=True)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///instance/db.sqlite3')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='tenant')
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    address = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    unit_number = Column(String)
    rent_amount = Column(Float)
    status = Column(String, default='vacant')

class Lease(Base):
    __tablename__ = 'leases'
    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('units.id'))
    tenant_id = Column(Integer, ForeignKey('users.id'))
    rent_amount = Column(Float)
    start_date = Column(String)
    end_date = Column(String)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('users.id'))
    unit_id = Column(Integer, ForeignKey('units.id'))
    amount = Column(Float)
    status = Column(String)
    method = Column(String)
    tx_ref = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MaintenanceTicket(Base):
    __tablename__ = 'maintenance_tickets'
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('users.id'))
    unit_id = Column(Integer, ForeignKey('units.id'))
    title = Column(String)
    description = Column(Text)
    status = Column(String, default='open')
    priority = Column(String, default='normal')
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    create_tables()
    print('Tables created')
