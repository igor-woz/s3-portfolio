import json
import boto3

sesClient = boto3.client('ses')

RECEIVER = "<RECEIVE_EMAIL>"
SENDER = "SEND_FROM_EMAIL"


def lambda_handler(event, context):

    data = json.loads(event.get('body'))
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    
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
            "Access-Control-Allow-Origin": "yourdomain.com"
        },
        'body': json.dumps({"result": "Success"}),
    }
