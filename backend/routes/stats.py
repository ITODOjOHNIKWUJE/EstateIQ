# backend/routes/stats.py
from flask import jsonify
from models import SessionLocal, Property, Unit, Lease, Payment, User
from datetime import datetime

def init_stats_routes(app):
    @app.route('/api/stats/overview', methods=['GET'])
    def stats_overview():
        db = SessionLocal()
        try:
            total_properties = db.query(Property).count()
            total_units = db.query(Unit).count()
            total_tenants = db.query(User).filter(User.role == 'tenant').count()
            total_leases = db.query(Lease).count()

            # Occupied units
            occupied_units = db.query(Unit).filter(Unit.status == 'occupied').count()
            occupancy_rate = 0
            if total_units > 0:
                occupancy_rate = round((occupied_units / total_units) * 100, 2)

            # Monthly income: sum of payments in current month (paid)
            now = datetime.utcnow()
            first_of_month = datetime(now.year, now.month, 1)
            monthly_sum = db.query(Payment).filter(Payment.created_at >= first_of_month, Payment.status.in_(['paid','Paid','PAID'])).all()
            monthly_total = sum(p.amount or 0 for p in monthly_sum)

            return jsonify({
                "total_properties": total_properties,
                "total_units": total_units,
                "total_tenants": total_tenants,
                "total_leases": total_leases,
                "occupied_units": occupied_units,
                "occupancy_rate": occupancy_rate,
                "monthly_income": monthly_total
            })
        finally:
            db.close()

    @app.route('/api/stats/income_by_months', methods=['GET'])
    def income_by_months():
        """
        Return last 12 months income totals: [{"month":"2024-10","total":12345}, ...]
        """
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            months = []
            for i in range(11, -1, -1):
                # compute year-month for i months ago
                year = (now.year if now.month - i > 0 else now.year - 1)
                month = (now.month - i - 1) % 12 + 1
                # first and last day approximations
                start = datetime(year, month, 1)
                if month == 12:
                    end = datetime(year + 1, 1, 1)
                else:
                    end = datetime(year, month + 1, 1)
                payments = db.query(Payment).filter(Payment.created_at >= start, Payment.created_at < end, Payment.status.in_(['paid','Paid','PAID'])).all()
                total = sum(p.amount or 0 for p in payments)
                months.append({"month": f"{start.year}-{start.month:02d}", "total": total})
            return jsonify(months)
        finally:
            db.close()
