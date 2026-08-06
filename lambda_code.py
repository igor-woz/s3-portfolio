import json
import boto3

sesClient = boto3.client('ses')

RECEIVER = "wozniakigor4@gmail.com"
SENDER = "contact@igorwozlab.org"


def lambda_handler(event, context):
    
    params = {"Source": SENDER,
            "Destination": 
            {"ToAddresses": [RECEIVER]},
            "Message": {
                "Subject": {
                    "Data": "New Contact Form Submission: ${event.name}",
                    "Charset": "UTF-8"
                },
                "Body": {
                    "Text": {
                        "Data": "Name: ${event.name}, Email: ${event.email}, Subject: ${event.subject}, Message: ${event.maessage}",
                        "Charset": "UTF-8"
                    }
                }
            }
    }

    sesClient.send_email()

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({"result": "Success"}),
    }
