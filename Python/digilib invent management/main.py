from flask import Flask, request, jsonify, render_template, send_file, redirect, make_response, url_for,abort, session, render_template_string
import pymongo
from flask_wtf import FlaskForm, CSRFProtect
from gridfs import GridFS
from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
from io import BytesIO
from flask_wtf.csrf import validate_csrf, generate_csrf
import random, string
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'im good im feeling allright'
csrf = CSRFProtect(app)
mongo_uri = "mongodb://192.168.15.10:27017"
client = pymongo.MongoClient(mongo_uri)

db = client['wtf_storage']
fs = GridFS(db)
files_collection = db['files']

MAX_FILE_SIZE_MB = 20  

class DeleteForm(FlaskForm):
    pass
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE=False,
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)

def custom_json_serializer(obj):
    """Custom decoder for objects"""
    if obj.__class__.__name__ == 'ObjectId':
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

@app.before_request
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = generate_csrf()
        
@app.route('/', methods=['GET'])
def show_upload_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_file():
    file =  request.files.get('file-attachment')
    uploader = request.form.get('uploader') 
    code_prefix = request.form.get('code_prefix')
    title = request.form.get('title')
    description = request.form.get('description')
    unique_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    unique_key = code_prefix + unique_key
    
    if not file:
        return jsonify({'error': 'No selected file'}), 400
    
    if file.content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
        return jsonify({'error': 'File size exceeds 20MB limit'}), 413
    
    file_metadata = {
        'file': file.filename,
        'title': title, 
        'uploader': uploader,  
        'description': description,
        'code': unique_key, 
        'timestamp': datetime.now().isoformat()
    }
    try:
        file_id = fs.put(file.stream, filename=file.filename, code=unique_key)
        files_collection.insert_one(file_metadata)
        return jsonify({'message': f'File {file.filename} with code {unique_key} uploaded successfully.', 'fileId': str(file_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check', methods=['GET'])
def check_files():  
    files_cursor = files_collection.find({})
    files = []
    delete_forms = {}
    for file_doc in files_cursor:
        file_doc['_id'] = str(file_doc['_id'])
        timestamp = datetime.strptime(file_doc['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
        file_doc['timestamp'] = timestamp.strftime("%Y-%m-%d %I:%M:%S %p")
        files.append(file_doc)

    return render_template('check_files.html', files=files)

@app.route('/download/<string:file_code>')
def download_file(file_code):
    print(f"Attempting to download file with code: {file_code}")
    try:
        file = fs.find_one({"code": file_code})
        if file is None:
            return make_response(jsonify({'error': 'File not found'}), 404)
        
        file_data = BytesIO(file.read())
        
        response = make_response(send_file(file_data, as_attachment=True, download_name=file.filename, mimetype="multipart/form-data"))
        response.headers.set('Content-Disposition', f'attachment; filename={file.filename}')
        
        return response
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    
@app.route('/delete/<string:file_code>', methods=['POST'])
def delete_file(file_code):
    try:
        grid_out = fs.find_one({"code": file_code})
        if grid_out is not None:
            # Delete the file from GridFS using its _id
            fs.delete(grid_out._id)
            
            # Now, delete the corresponding metadata from the files_collection
            files_collection.delete_one({"code": file_code})
            
            # Redirect back to the check_files route after deletion
            return redirect(url_for('check_files')), 303
        else:
            # Handle the case where the file is not found
            return "File not found.", 404
    except Exception as e:
        # Handle exceptions
        return str(e), 500
    
@app.route('/edit/<string:file_code>', methods=['GET'])
def show_edit_form(file_code):
    file = files_collection.find_one({'code': file_code})
    if not file:
        abort(404) 
    return render_template('edit_file.html', file=file)

@app.route('/update/<string:file_code>', methods=['POST'])
def update_file(file_code):
    title = request.form.get('title')
    uploader = request.form.get('uploader')
    description = request.form.get('description')
    file_newname = request.form.get('file-name')
    
    update_result = files_collection.update_one(
        {'code': file_code},
        {'$set': {'title': title, 'uploader': uploader, 'description': description, 'file': file_newname}}
    )
    if update_result.modified_count > 0:
        return redirect(url_for('check_files')), 303
    else:
        return "File not found or no changes made.", 404
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
