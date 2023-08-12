from flask import Flask
from flask import request
from flask import Response
from flask import make_response
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

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    print("WhatsApp Webhook starting...")
    print(request.args)
    print("WhatsApp Webhook completed ✅")
    if request.args.get("hub.challenge"):
        return request.args.get("hub.challenge")
    else:
        json_data = json.loads(request.data)
        print("Message Data Received:")
        
        print("json_data:")
        print(type(json_data))
        print(json_data)
        
        print("request.data:")
        print(type(request.data))
        print(request.data)

        data_decoded = request.data.decode('utf-8')
        print("request.data.decode('utf-8')")
        print(type(data_decoded))
        print(data_decoded)

        if json_data["entry"]:
            if json_data["entry"][0]:
                if json_data["entry"][0]["changes"]:
                    if json_data["entry"][0]["changes"][0]:
                        if json_data["entry"][0]["changes"][0]["value"]:
                            if json_data["entry"][0]["changes"][0]["value"]["messages"]:
                                if json_data["entry"][0]["changes"][0]["value"]["messages"][0]:
                                    reply()
        else:
            response = make_response('')
            response.status_code = 200
            return response

def reply():
    url = "https://graph.facebook.com/v17.0/116111058231877/messages"
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": "528116916048",
        "text": {
            "body": "This is a sample message sent by the Flask app hosted on Vercel"
        }
    })
    WHATSAPP_API_TEMP_ACCESS_TOKEN = os.environ.get('WHATSAPP_API_TEMP_ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {WHATSAPP_API_TEMP_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    response_json = response.json()
    print(response_json)

    response = make_response(response_json)
    response.status_code = 200
    return response

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
