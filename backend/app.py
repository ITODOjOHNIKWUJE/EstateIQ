# backend/app.py
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

    # ✅ Strong CORS policy that properly responds to preflight (OPTIONS) requests
    #    Allows your Vercel frontend, localhost (dev), and the API host itself.
    CORS(
        app,
        resources={r"/api/*": {"origins": [
            "https://estate-iq-zeta.vercel.app",
            "http://localhost:3000",
            "https://estateiq-api-7eky.onrender.com"
        ]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Initialize DB and routes
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
        return jsonify({'message': 'Welcome to EstateIQ API'})

    return app

if __name__ == '__main__':
    app = create_app()
    # Render commonly uses PORT env var; use 10000 as a safe default locally if needed
    port = int(os.environ.get("PORT", 10000))
    # Bind to all interfaces so Render can detect the open port and accept connections
    app.run(host="0.0.0.0", port=port, debug=False)
