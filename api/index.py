from flask import Flask
from flask import request
import requests
import uuid


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
    FIREBASE_SERVER_KEY = os.getenv('FIREBASE_SERVER_KEY')
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

    response = requests.post(url, headers=headers, json=data)
    return response.content, response.status_code
