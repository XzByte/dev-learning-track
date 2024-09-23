import os
import uuid
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv

from passlib.hash import bcrypt
from functools import wraps
import flask_monitoringdashboard as dashboard
import pytz

app = Flask(__name__)

def generate_api_key():
    return str(uuid.uuid4())

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key:
            return jsonify({"error": "API key is missing"}), 401
        user = mongo.cx['account']['user_data'].find_one({"api_key": api_key})
        if not user:
            return jsonify({"error": "Invalid API key"}), 401
        
        utc = pytz.UTC
        user_expires_at_utc = utc.localize(user['api_key_expiration'])
        
        if user_expires_at_utc < datetime.now(timezone.utc):
            return jsonify({"error": "Expired API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return "Welcome to the rate-limited Flask app!"

@app.route('/test')
def test():
    return jsonify("You've done better!")

if __name__ == '__main__':
    dashboard.bind(app)
    app.run(host='0.0.0.0', port=5000)