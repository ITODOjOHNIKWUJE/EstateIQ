# backend/app.py
from flask import Flask, jsonify, request, make_response
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

    # ✅ Full CORS setup for Vercel frontend & local dev
    CORS(
        app,
        resources={r"/api/*": {"origins": [
            "https://estate-iq-zeta.vercel.app",
            "http://localhost:3000"
        ]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # ✅ Database and routes
    create_tables()
    init_auth_routes(app)
    init_user_routes(app)
    init_property_routes(app)
    init_tenant_routes(app)
    init_lease_routes(app)
    init_stats_routes(app)
    init_payment_routes(app)
    init_maintenance_routes(app)

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
            response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
            response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
            return response, 200

    @app.route('/')
    def home():
        return jsonify({'message': 'Welcome to EstateIQ API'}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
