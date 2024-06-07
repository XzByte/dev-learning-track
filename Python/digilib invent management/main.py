from flask import Flask, request, jsonify, render_template, send_file, abort
import pymongo
from gridfs import GridFS
from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
import json
from io import BytesIO
from bson import ObjectId
import random, string
app = Flask(__name__)

mongo_uri = "mongodb://192.168.15.10:27017"
client = pymongo.MongoClient(mongo_uri)

db = client['wtf_storage']
fs = GridFS(db)

files_collection = db['files']

MAX_FILE_SIZE_MB = 20  

def custom_json_serializer(obj):
    """Custom decoder for objects"""
    if obj.__class__.__name__ == 'ObjectId':
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

@app.route('/', methods=['GET'])
def show_upload_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_file():
    file = request.files.get('file-attachment')
    uploader = request.form.get('uploader') 
    code_prefix = request.form.get('code')
    title = request.form.get('title')
    description = request.form.get('description')
    unique_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    if not file:
        return jsonify({'error': 'No file part'}), 400
    
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
        file_id = fs.put(file.stream, filename=file.filename)
        files_collection.insert_one(file_metadata)
        return jsonify({'message': f'File {file.filename} uploaded successfully.', 'fileId': str(file_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/check', methods=['GET'])
def check_files():
    files_cursor = files_collection.find({})
    files = []
    for file_doc in files_cursor:
        file_doc['_id'] = str(file_doc['_id'])
        timestamp = datetime.strptime(file_doc['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
        file_doc['timestamp'] = timestamp.strftime("%Y-%m-%d %I:%M:%S %p")
        files.append(file_doc)
    return render_template('check_files.html', files=files)

@app.route('/download/<string:file_title>')
def download_file(file_title):
    print(f"Attempting to download file with title: {file_title}") 
    try:
        file = fs.find_one({"filename": file_title})
        if file is None:
            return jsonify({'error': 'File not found'}), 404
        file_data = BytesIO(file.read())
        return send_file(file_data, as_attachment=True, download_name=file.filename, mimetype='application/octet-stream')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
