import json
import boto3
import os
import urllib.request
import urllib.parse

# create an SES Client to send the email
sesClient = boto3.client('ses')

# get all of the environment variables
RECEIVER = os.environ.get('ReceiverEmail')
SENDER = os.environ.get('SenderEmail')
TURNSTILE_SECRET_KEY = os.environ.get("TurnstileKey")
TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

# function to verify the Cloudflare captcha
def verify_turnstile(token, remote_ip=None):
    payload = {
        "secret": TURNSTILE_SECRET_KEY,
        "response": token,
    }
    if remote_ip:
        payload["remoteip"] = remote_ip

    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(TURNSTILE_VERIFY_URL, data=data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result.get("success", False)
    except Exception:
        
        return False


def lambda_handler(event, context):

    data = json.loads(event.get('body'))
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    token = data.get("cfToken")
    source_ip = event.get("requestContext", {}).get("identity", {}).get("sourceIp")

    if not token or not verify_turnstile(token, source_ip):
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"result": "Captcha verification failed"})
        }
    
    params = {"Source": SENDER,
            "Destination": 
            {"ToAddresses": [RECEIVER]},
            "Message": {
                "Subject": {
                    "Data": f"New Contact Form Submission From: {name}",
                    "Charset": "UTF-8"
                },
                "Body": {
                    "Text": {
                        "Data": f"Name: {name}, Email: {email}, Subject: {subject}, Message: {message}",
                        "Charset": "UTF-8"
                    }
                }
            }
    }

    sesClient.send_email(**params)

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "https://www.igorwozlab.org"
        },
        'body': json.dumps({"result": "Success"}),
    }
