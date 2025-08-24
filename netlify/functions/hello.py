import json

def handler(event, context):
    body = {
        "message": "Hello from Hardonia API 🚀",
        "event": event,
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
