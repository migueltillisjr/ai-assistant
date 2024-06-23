#!/usr/bin/env python3.11
from CoreService import main
from flask import Flask, jsonify, request, render_template
from functools import wraps
from gen_report import initiate
from BrevoSend  import build_campaign, return_campaign_files, delete_campaign_files
from BrevoWorkflow import adhoc_build_campaign
from BrevoUpdateContactList  import brevo_load_contacts
from BrevoBounceList import main as gen_bounce_list
from assistant import Assistant
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
    AI = Assistant()
    AI.send_message(data['message'])
    #AI.send_message(data)
    message = AI.wait_on_run()
    return jsonify({"message": message})



@app.route('/results', methods=['GET'])
def render_page_with_request():
    #initiate()
    return render_template('campaign_report.html')
    #return render_template('report_template.html')

    #url_query = request.args.get('query', False)
    #if url_query:
    #    return render_template('index.html')
    #else:
    #    return jsonify({"error": "Unauthorized"}), 401


@app.route('/delete_campaigns', methods=['POST'])
#@require_api_key  # Require API key for this POST route
def delete_campaigns():
    filenames_to_delete=list()
    data = request.json
    delete_campaign_files(data['campaigns'])
    return jsonify({"response": "OK"})


@app.route('/list_campaigns', methods=['GET'])
#@require_api_key  # Require API key for this POST route
def list_campaigns():
    filenames=list()
    #data = request.json
    campaign_files = return_campaign_files()
    return jsonify({"response": campaign_files})


@app.route('/query', methods=['POST'])
#@require_api_key  # Require API key for this POST route
def post_example():
    data = request.json
    #if 'emails' in data.keys():
    #    if data['emails']:
    #        brevo_load_contacts(adhoc_contacts=data['emails'])
    if ('subject' in data.keys()) and ('scheduledAt' in data.keys()):
        adhoc_build_campaign(data)
    return jsonify({"response": "OK"})

    #return jsonify({"response": data})
    #return jsonify({"response": main(data)})


@app.route('/upload_contacts', methods=['POST'])
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


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the content from the request
        content = request.get_data().decode('utf-8')  # Decode bytes to string

        # Remove quotation marks from the beginning and end of the string
        content = content.strip('"')

        # Write the content to a file
        with open('/var/www/html/uploads/email-design.html', 'w') as f:  # Using 'w' mode since content is string
            f.write(content)

        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
