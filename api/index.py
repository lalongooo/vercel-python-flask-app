from flask import Flask
from flask import request
from flask import Response
from flask import make_response
import requests
import uuid
import os
import json
from utils.util import Util
from utils.constants import (
    GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL,
    HEADERS,
    WHATSAPP_API_TEMP_ACCESS_TOKEN,
)


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
    if request.args.get("hub.challenge"):
        return request.args.get("hub.challenge")
    else:
        json_data = json.loads(request.data)
        print("Message Data Received:")

        data_decoded = request.data.decode('utf-8')
        print("request.data.decode('utf-8')")
        print(type(data_decoded))
        print(data_decoded)

        if Util.is_message(request):
            return reply_with_interactive_message()
        else:
            response = make_response('')
            response.status_code = 200
            return response

def reply_with_interactive_message():
    url = GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL

    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": "528116916048",
        "type": "interactive",
        "recipient_type": "individual",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "header text"
            },
            "body": {
                "text": "body text"
            },
            "footer": {
                "text": "footer text"
            },
            "action": {
                "button": "Select an option",
                "sections":[{
                    "title":"your-section-title-content",
                    "rows": [{
                        "id": "1",
                        "title": "row-title-content",
                        "description": "row-description-content",           
                    }]
                },
                {
                    "title":"your-section-title-content",
                    "rows": [{
                        "id": "2",
                        "title": "row-title-content",
                        "description": "row-description-content",           
                    }]
                }]
            }
        }
    })

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    print(response.text)

def reply():
    url = GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": "528116916048",
        "text": {
            "body": "This is a sample message sent by the Flask app hosted on Vercel"
        }
    })

    response = requests.request("POST", url, headers=HEADERS, data=payload)
    
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
