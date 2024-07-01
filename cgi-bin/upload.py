#!/usr/bin/env python3
import cgi
import os
import boto3
import cv2
import numpy as np
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

print("Content-Type: text/html")
print()

# Hardcode AWS credentials (not recommended for production)
AWS_ACCESS_KEY = 'AKIAW3MD77ORGHCKUJ6F'
AWS_SECRET_KEY = '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'
AWS_REGION = 'ap-south-1'

def launch_instances(num_instances):
    ec2_client = boto3.client(
        'ec2',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    ec2_client.run_instances(
        ImageId='ami-0e1d06225679bc1c5',  # Update with your preferred AMI ID
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=num_instances
    )

def count_fingers(image_path):
    print(f"Processing image for finger count: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to read image.")
        return 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (35, 35), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(cnt)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        if defects is not None:
            count_defects = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                a = np.linalg.norm(np.array(start) - np.array(end))
                b = np.linalg.norm(np.array(start) - np.array(far))
                c = np.linalg.norm(np.array(end) - np.array(far))
                angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57
                if angle <= 90:
                    count_defects += 1
            print(f"Detected {count_defects + 1} fingers.")
            return count_defects + 1
    print("No fingers detected.")
    return 0

form = cgi.FieldStorage()
fileitem = form['image']

if fileitem.filename:
    filepath = os.path.join('/var/www/html/uploads', fileitem.filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(fileitem.file.read())
	
    print(f"File uploaded: {filepath}")

    num_fingers = count_fingers(filepath)
    try:
        launch_instances(num_fingers)
        print(f"File uploaded and {num_fingers} instances launched successfully!")
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found. Please configure them properly.")
	print(f"Error: {e}")
else:
    print("No file was uploaded.")

