from flask import request, jsonify
from models import SessionLocal, create_tables, User
import bcrypt

create_tables()

def init_user_routes(app):
    pass
