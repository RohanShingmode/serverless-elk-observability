import json
import boto3
import urllib3

s3 = boto3.client('s3')
http = urllib3.PoolManager()

# Update with your active EC2 Target Address
ELASTIC_URL = "http://YOUR_EC2_PUBLIC_IP:9200/logs-index/_doc"

def lambda_handler(event, context):
    # Parse object locations from inbound bucket event metadata
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Extract file contents from target storage node
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')

    headers = {'Content-Type': 'application/json'}

    # Process and stream line-by-line log data to indices
    for line in file_content.splitlines():
        if line.strip(): 
            r = http.request('POST', ELASTIC_URL, body=line, headers=headers)
            print(f"Ingestion API Response Status: {r.status}")
                
    return {"statusCode": 200, "body": "Log Stream Completed Successfully"}