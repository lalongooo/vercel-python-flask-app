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

@app.route('/whatsapp', methods=['GET'])
def whatsapp():
    print("WhatsApp Webhook starting...")
    print(request.args)
    print("WhatsApp Webhook completed ✅")

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    deviceToken = request.headers.get('Device-Token')
    FIREBASE_FCM_SEND_URL = 'https://fcm.googleapis.com/fcm/send'
    FIREBASE_SERVER_KEY = os.environ.get('FIREBASE_SERVER_KEY')
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
    firebaseResponse = requests.post(FIREBASE_FCM_SEND_URL, headers=headers, json=data)

    response = Response(
        response=firebaseResponse.content,
        status=firebaseResponse.status_code,
        mimetype="application/json"
    )
    return response
