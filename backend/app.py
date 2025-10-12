from flask import Flask, jsonify
from flask_cors import CORS
from routes.users import init_user_routes
from routes.properties import init_property_routes
from routes.payments import init_payment_routes
from routes.stats import init_stats_routes
from routes.maintenance import init_maintenance_routes
from routes.auth import init_auth_routes
from routes.tenants import init_tenant_routes
from routes.leases import init_lease_routes
from models import create_tables
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'estateiq-dev-secret')

    # ✅ Enable CORS for all routes and origins (fixes “Network Error” on Vercel)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    create_tables()
    init_auth_routes(app)
    init_user_routes(app)
    init_property_routes(app)
    init_tenant_routes(app)
    init_lease_routes(app)
    init_stats_routes(app)
    init_payment_routes(app)
    init_maintenance_routes(app)

    @app.route('/')
    def home():
        return jsonify({'message': 'Welcome to EstateIQ API - CORS Fixed ✅'})

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
