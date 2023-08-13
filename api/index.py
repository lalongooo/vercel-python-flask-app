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

@app.route('/privacy')
def privacy():
    return '''
Effective Date: Aug 12th 2023

This Privacy Policy explains how Fivra ("we," "us," or "our") collects, uses, and protects the personal information of our customers ("users" or "you"). We are committed to safeguarding your privacy and ensuring the security of the information you provide to us. By using our internet services, you agree to the terms outlined in this Privacy Policy.

1. Information We Collect

We only collect the minimal amount of information necessary to provide and manage our internet services. This information may include:

Contact Information: Name, email address, and phone number.
Service Information: Account details, service plans, and billing information.
Technical Information: IP address, device information, browser type, and operating system.
Usage Data: Data about your usage of our internet services, such as bandwidth usage, connection logs, and session duration.
2. Use of Information

We use the collected information solely for the purpose of providing, maintaining, and improving our internet services. Specifically, we may use your information for:

Notifying you about the status of your internet service, including updates, maintenance, and outages.
Delivering important information about your account, billing, and service plans.
Analyzing usage patterns to optimize network performance and quality of service.
Resolving technical issues and responding to your inquiries.
Complying with legal and regulatory requirements.
3. Information Sharing

We do not sell, rent, or lease your personal information to third parties. However, we may share your information with:

Service Providers: We may share data with trusted third-party service providers who assist us in delivering our services (e.g., customer support, billing, technical support).

Legal Requirements: We may disclose information if required by law, subpoena, court order, or government request.

Business Transfers: In the event of a merger, acquisition, or sale of all or a portion of our assets, your information may be transferred to the acquiring entity.

4. Data Security

We implement appropriate technical and organizational measures to protect your personal information from unauthorized access, disclosure, alteration, or destruction. While we strive to ensure the security of your data, no method of transmission over the internet or electronic storage is completely secure. We cannot guarantee absolute security.

5. Your Choices

You have the right to:

Access and Update: Access, correct, or update your personal information by contacting us.
Opt-Out: You can opt-out of receiving non-essential communications from us.
6. Children's Privacy

Our services are not intended for children under the age of 13. We do not knowingly collect or maintain information from individuals under 13 years of age.

7. Changes to this Privacy Policy

We may update this Privacy Policy from time to time. Any changes will be posted on our website, and the revised policy will be effective upon posting.

8. Contact Us

If you have any questions or concerns about our Privacy Policy or the use of your personal information, please contact us at [contact email/phone number].

By using our services, you acknowledge that you have read, understood, and agree to this Privacy Policy.    
    '''


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
            print("it is message")
            author = Util.get_author(request)
            if Util.is_interactive_list_reply(request):
                print("it is interactive reply")
                return handle_interactive_list_reply(request)
                # response = make_response('it is an interactive reply')
                # response.status_code = 200
                # return response
            else:
                print("it is NOT interactive reply")
                return reply_with_interactive_message(author)
        else:
            print("it is not a valid message")
            response = make_response('')
            response.status_code = 200
            return response

def handle_interactive_list_reply(request):
    reply_content = Util.get_interactive_reply(request)
    print(reply_content)
    response = make_response(reply_content)
    response.status_code = 200
    return response

def reply_with_interactive_message(to_author):
    url = GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL

    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": to_author,
        "type": "interactive",
        "recipient_type": "individual",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "¡Hola! Muchas gracias por ponerte en contacto con nosotros."
            },
            "body": {
                "text": "Estamos encantados de ayudarte."
            },
            "action": {
                "button": "Elige una opción",
                "sections":
                [
                    {
                        "rows":
                        [
                            {
                                "id": "1",
                                "title": "Contratar servicio",
                                "description": "Conoce los detalles para contratar internet en tu domicilio"
                            },
                            {
                                "id": "2",
                                "title": "Reportar una falla",
                                "description": "Lamentamos que esto haya sucedido. Selecciona para levantar un reporte"
                            },
                            {
                                "id": "3",
                                "title": "Precios de paquetes",
                                "description": "Información relacionada a precios de paquetes de internet en tu casa"
                            }
                        ]
                    }
                ]
            }
        }
    })

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    response_json = response.json()
    print(response_json)

    response = make_response(response_json)
    response.status_code = 200
    return response

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
