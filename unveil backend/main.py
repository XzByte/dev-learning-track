from flask import Flask, request, jsonify, make_response, redirect, render_template, flash, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymongo
import requests 
from functools import wraps
app = Flask(__name__)
from requests.exceptions import RequestException
app.secret_key = 'so-secret'

api_url = ''

limiter_unauth = Limiter(get_remote_address, default_limits="20 per week") # idk this function are working or not, but the app can be initated


limiter_auth = Limiter(key_func=lambda: session.get('access_token'), default_limits="20 per day") # same here

limiter_auth.init_app(app)
limiter_unauth.init_app(app)

def is_authenticated():
    # Simulate authentication check
    return request.headers.get("X-Authenticated-User") is not None

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            flash('Please log in first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/signup', methods=['GET', 'POST'])
@limiter_auth.limit("20 per day")
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        data = {
            'username': username,
            'email': email,
            'password': password
        }
        
        response = requests.post(api_url+'signup', json=data)
                
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        response = requests.post(api_url+'login', json={'username': username, 'password': password})
        
        if response.status_code == 200:
            login_response = response.json()
            access_token = login_response.get('access_token')
            secret_key = login_response.get('secret_key')
            
            # creating session based from output        
            session['access_token'] = access_token
            session['secret_key'] = secret_key
            
            return redirect(url_for('protected'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/protected')
@limiter_auth.limit("20 per day")
@require_login
def protected():
    if 'access_token' in session:
        return 'Welcome to the protected area!'
    else:
        flash('Please log in first.')
        return redirect(url_for('login'))
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
