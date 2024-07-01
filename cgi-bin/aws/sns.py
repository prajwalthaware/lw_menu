#!/usr/bin/python3
print("Access-Control-Allow-Origin: *")
print("Access-Control-Allow-Methods: POST, GET, OPTIONS")
print('Content-Type: text/html')
print()
import boto3
import cgi

access_key = 'AKIAW3MD77ORLVBH5WKO'
secret_key = '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'

session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name='ap-south-1'
)

sns_client = session.client('sns')

form = cgi.FieldStorage()
name=form.getvalue('name')

response = sns_client.create_topic(Name=name)
print("Topic ARN:", response['TopicArn'])
