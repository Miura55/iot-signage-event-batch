import os
import json
import http.client
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

iot = boto3.client('iot-data')
parameter_store = boto3.client('ssm')

def handler(event, context):
    # Parameter StoreからAPIキーを取得
    try:
        response = parameter_store.get_parameter(Name='/iot-signage/OPENWEATHER_API_KEY', WithDecryption=True)
        api_key = response['Parameter']['Value']
    except ClientError as e:
        print("Failed to get parameter: " + e.response['Error']['Message'])
        return {
            "statusCode": 500,
            "body": json.dumps(event)
        }
    
    # OpenWeatherMap APIを使って天気情報を取得
    city = os.environ.get("CITY", "Tokyo,JP")
    conn = http.client.HTTPConnection("api.openweathermap.org")
    conn.request("GET", f"/data/2.5/weather?q={city}&units=metric&appid={api_key}", '', {})
    res = conn.getresponse()
    raw_data = res.read()
    data = json.loads(raw_data.decode("utf-8"))
    
    # IoT CoreにメッセージをPublish
    try:
        event_datetime = datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%SZ")
        publish_payload = {
            "datetime": event_datetime.strftime("%m/%d %H:%M"),
            "weather": data["weather"][0]["main"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
        }
        iot.publish(
            topic="signage/msg",
            qos=1,
            payload=json.dumps(publish_payload)
        )
    except ClientError as e:
        print("Failed to publish message: " + e.response['Error']['Message'])
        return {
            "statusCode": 500,
            "body": json.dumps(event)
        } 
    
    print("Publish payload: " + json.dumps(publish_payload, indent=2))
    return {
        "statusCode": 200,
        "body": json.dumps(event)
    }
