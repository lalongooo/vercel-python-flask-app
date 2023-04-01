from flask import Flask
from flask import request
from flask import Response
import requests
import uuid
import os
import json


app = Flask(__name__)


@app.route('/')
def home():
    return 'Home Page Route'


@app.route('/about')
def about():
    return 'About Page Route'


@app.route('/portfolio')
def portfolio():
    return 'Portfolio Page Route'


@app.route('/contact')
def contact():
    return 'Contact Page Route'


@app.route('/api')
def api():
    with open('data.json', mode='r') as my_file:
        text = my_file.read()
        return text

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    deviceToken = request.headers.get('Device-Token')
    url = 'https://fcm.googleapis.com/fcm/send'
    FIREBASE_SERVER_KEY = os.environ.get('FIREBASE_SERVER_KEY')
    print("Read ENV var")
    print(os.environ.get('FIREBASE_SERVER_KEY'))
    print("Finished reading ENV var")
    headers = {        
        'Authorization': f'key={FIREBASE_SERVER_KEY}',
        'Content-Type': 'application/json'
    }
    generated_nonce = str(uuid.uuid4())
    data = {
        'to': deviceToken,
        'data': {
            'default': {
                'nonce': generated_nonce
            }
        }
    }

    

    # Make HTTP request to the Firebase Messaging Service
    firebaseResponse = requests.post(url, headers=headers, json=data)

    response = Response(
        response=firebaseResponse.content,
        status=200,
        mimetype="text/plain"
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[os.getenv('FIREBASE_SERVER_KEY')] = FIREBASE_SERVER_KEY
    return response
