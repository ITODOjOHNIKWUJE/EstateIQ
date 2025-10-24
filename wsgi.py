# wsgi.py
from backend.app import app  # import the Flask app correctly

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # only for local testing
