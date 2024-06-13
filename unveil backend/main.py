
from flask import Flask, request, jsonify, make_response, redirect, render_template, flash, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymongo
import requests 
app = Flask(__name__)
from requests.exceptions import RequestException
secret_key = 'so-secret'
api_url = ''

# Flask-Limiter Configuration
# limiter = Limiter(
#     app=app,
#     key_func=get_remote_address,
#     default_limits=["5 per day","20 per day"]
# )

def is_authenticated():
    # Simulate authentication check
    return request.headers.get("X-Authenticated-User") is not None

# @app.route("/api/data")
# @limiter.limit("20/day;5/day", key_func=lambda: "authenticated" if is_authenticated() else "unauthenticated")
# def get_data():
#    
#     return jsonify({"message": "Data retrieved successfully"})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Capture form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Prepare the data to be sent to the external API
        data = {
            'username': username,
            'email': email,
            'password': password
        }
        
        # Send the data to the external API
        response = requests.post(api_url+'signup', json=data)
        
        # Redirect to login page after signup attempt, regardless of outcome
        
        return redirect(url_for('login'))
    # Render the signup form on GET request
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Send credentials to the external login API
        response = requests.post(api_url+'login', json={'username': username, 'password': password})
        
        if response.status_code == 200:
            login_response = response.json()
            # access_token = login_response.get('access_token')
            # token_type = login_response.get('token_type')
            # secret_key = login_response.get('secret_key')
            print(login_response) 
            
            # Store tokens in session for demonstration purposes
            # session['access_token'] = access_token
            # session['username'] = username
            # session['secret_key'] = secret_key
            
            # Redirect to a protected route or show a success message
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/protected')
def protected():
    if 'access_token' in session:
        return 'Welcome to the protected area!'
    else:
        flash('Please log in first.')
        return redirect(url_for('login'))
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
