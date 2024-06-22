from flask import Flask, request, jsonify, make_response, redirect, render_template, flash, session, url_for
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
import requests 
from functools import wraps
app = Flask(__name__)
from requests.exceptions import RequestException
import os 
from dotenv import load_dotenv
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
api_url = os.getenv('API_URL')

# limiter_unauth = Limiter(get_remote_address, default_limits="20 per week") # idk this function are working or not, but the app can be initated


# limiter_auth = Limiter(key_func=lambda: session.get('access_token'), default_limits="20 per day") # same here

# limiter_auth.init_app(app)
# limiter_unauth.init_app(app)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    return(render_template('index.html'))

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
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

@app.route('/submit-page')
def submit_page():
    if 'access_token' in session:
        return render_template('submit.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/scan', methods=['POST'])
def scan():
    if 'access_token' in session:
        file = request.files['file']
        if file and file.filename:
            headers = {'Authorization': f'Bearer {session["access_token"]}'}
            upload_response = requests.post(api_url+'uploadfile', headers=headers, files={'file': (file.filename, file, file.content_type)})
            
            if upload_response.status_code == 200:
                result = upload_response.json()
                art = result.get('detail').get('content')[0].get('art')
                filename = result.get('detail').get('content')[0].get('filename')
                confidence_value = float(result.get('detail').get('content')[0].get('confidence'))
                print("Filename from server:", filename)
                rounded_confidence = round(confidence_value, 2) 
                confidence = "{:.2%}".format(rounded_confidence)

                
                session['art'] = art
                session['filename'] = filename
                session['confidence'] = confidence
                return redirect(url_for('result'))
            else:
                return jsonify({"error": "Upload failed"}), 400
        else:
            return jsonify({"error": "No file selected"}), 400
    else:
        return jsonify({"error": "Cannot upload file without a valid token."}), 401
    
@app.route('/result')
def result():
    art = session.get('art')
    filename = session.get('filename')
    confidence = session.get('confidence')
    return render_template('result.html', art=art, filename=filename, confidence=confidence)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        response = requests.post(api_url+'login', json={'username': username, 'password': password})
        
        if response.status_code == 200:
            login_response = response.json()
            access_token = login_response.get('access_token')
            secret_key = login_response.get('secret_key')
        
            session['access_token'] = access_token
            session['secret_key'] = secret_key
            
            return redirect(url_for('submit_page'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/protected')
# @limiter_auth.limit("20 per day")
@require_login
def protected():
    if 'access_token' in session:
        return 'Welcome to the protected area!'
    else:
        flash('Please log in first.')
        return redirect(url_for('login'))
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)