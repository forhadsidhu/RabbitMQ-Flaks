import requests
import random
import json
import time
import csv
import base64
import os
# Generate a random base64-encoded image frame
def generate_image_frame():
    return str(base64.b64encode(os.urandom(10)), 'utf-8')

# Generate a random JSON body
def generate_json_body():
    num_preds = random.randint(1, 5)
    preds = []
    for i in range(num_preds):
        preds.append({
            'image_frame': generate_image_frame(),
            'prob': random.random(),
            'tags': ['tag1', 'tag2']
        })
        if preds[-1]['prob'] < 0.25:
            preds[-1]['tags'].append('low_prob')
    return {
        'device_id': 'device_' + str(random.randint(1, 10)),
        'client_id': 'client_' + str(random.randint(1, 5)),
        'created_at': str(time.time()),
        'data': {
            'license_id': 'license_' + str(random.randint(1, 20)),
            'preds': preds
        }
    }

# Send requests to the producer endpoint
num_requests = 1000
producer_url = 'http://producer:8000/predictions/'
for i in range(num_requests):
    json_body = generate_json_body()
    print(json_body)
    headers = {'Content-type': 'application/json'}
    response = requests.post(producer_url, json=json.dumps(json_body), headers=headers)
    if response.status_code != 200:
        print('Request failed with status code', response.status_code)
    time.sleep(0.1)

# Save data to CSV file
consumer_url = 'http://consumer:8000/csv/'
response = requests.get(consumer_url)
if response.status_code != 200:
    print('Request failed with status code', response.status_code)
else:
    data = response.json()
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data['headers'])
        for row in data['rows']:
            writer.writerow(row)
