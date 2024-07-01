#!/usr/bin/env python3

import cgi
import cgitb
import boto3
import os

# Enable debugging
cgitb.enable()

# Set AWS credentials as environment variables
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAW3MD77ORLVBH5WKO'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'

def create_bucket(bucket_name):
    try:
        s3 = boto3.client('s3', region_name='ap-south-1')
        s3.create_bucket(
            Bucket=bucket_name,
            ACL='private',
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        return "Bucket created successfully!"
    except Exception as e:
        return f"Error creating bucket: {str(e)}"

def list_buckets():
    try:
        s3 = boto3.client('s3', region_name='ap-south-1')
        buckets = s3.list_buckets()
        return [bucket['Name'] for bucket in buckets['Buckets']]
    except Exception as e:
        return []

def upload_file(bucket_name, fileitem):
    try:
        s3 = boto3.client('s3', region_name='ap-south-1')
        s3.upload_fileobj(fileitem.file, bucket_name, fileitem.filename)
        return "File uploaded successfully!"
    except Exception as e:
        return f"Error uploading file: {str(e)}"

def main():
    print("Content-Type: text/html")
    print()
    
    form = cgi.FieldStorage()
    action = form.getvalue("action")
    
    if action == "create_bucket":
        bucket_name = form.getvalue("bucket_name")
        if bucket_name:
            result = create_bucket(bucket_name)
            print(f"<h2>{result}</h2>")
    
    elif action == "upload_file":
        bucket_name = form.getvalue("bucket_name")
        fileitem = form['file']
        if bucket_name and fileitem.filename:
            result = upload_file(bucket_name, fileitem)
            print(f"<h2>{result}</h2>")
    
    buckets = list_buckets()
    print("""
    <html>
    <head>
        <title>Manage S3 Buckets</title>
    </head>
    <body>
        <h2>Create S3 Bucket</h2>
        <form action="/cgi-bin/bucket.py" method="post">
            <input type="hidden" name="action" value="create_bucket">
            <label for="bucket_name">Bucket Name:</label>
            <input type="text" id="bucket_name" name="bucket_name" required>
            <br><br>
            <input type="submit" value="Create Bucket">
        </form>
        <h2>Upload File to S3 Bucket</h2>
        <form action="/cgi-bin/bucket.py" method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="upload_file">
            <label for="bucket_name">Select Bucket:</label>
            <select id="bucket_name" name="bucket_name" required>
    """)
    
    for bucket in buckets:
        print(f'<option value="{bucket}">{bucket}</option>')
    
    print("""
            </select>
            <br><br>
            <label for="file">Choose File:</label>
            <input type="file" id="file" name="file" required>
            <br><br>
            <input type="submit" value="Upload File">
        </form>
    </body>
    </html>
    """)

if __name__ == "__main__":
    main()

