#!/usr/bin/env python3.11
from flask import Flask, jsonify, request, render_template
from functools import wraps
# from assistant import Assistant
from flask_cors import CORS

app = Flask(__name__, template_folder="/var/www/html/uploads")
CORS(app)

VALID_API_KEYS = {"2E-QUgCO&W-X9kaahj@I-EaQUgCO&W-X9kaahjby"}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')  # Route for the root URL
def home():
    return jsonify({"message": "Welcome to the API!"})


@app.route('/assistant', methods=['POST'])  # Route for the root URL
def assistant():
    data = request.json
    # AI = Assistant()
    # AI.send_message(data['message'])
    #AI.send_message(data)
    # message = AI.wait_on_run()
    # return jsonify({"message": message})
    return jsonify({"message": message})



@app.route('/upload', methods=['POST'])
def upload_contacts():
    try:
        # Check if the 'file' field is in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        # Check if a file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the file
        file_path = '/var/www/html/uploads/user_contacts.csv'
        file.save(file_path)

        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    run()