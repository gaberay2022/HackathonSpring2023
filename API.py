import boto3
import csv
import json


with open('santi-recog_accessKeys.csv', 'r') as file:
    next(file)
    reader = csv.reader(file)

    for line in reader:
        access_key_id = line[0]
        secret_access_key = line[1]

client = boto3.client('rekognition', region_name = 'us-east-2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

photo = 'paper.jpg'

with open(photo, 'rb') as image_file:
    source_bytes = image_file.read()

detect_objects = client.detect_labels(Image={'Bytes': source_bytes})

#print(detect_objects)

categories = []
for label in detect_objects['Labels']:
    for category in label['Categories']:
        categories.append(category['Name'])
        
print(categories)