import csv
import json
import os
from flask import Flask, jsonify, request
import pika

app = Flask(__name__)

@app.route('/csv/', methods=['GET'])
def get_csv():
    # Connect to RabbitMQ queue
    credentials = pika.PlainCredentials(os.getenv('RABBITMQ_DEFAULT_USER'), os.getenv('RABBITMQ_DEFAULT_PASS'))
    parameters = pika.ConnectionParameters(os.getenv('RABBITMQ_HOST'), os.getenv('RABBITMQ_PORT'), os.getenv('RABBITMQ_VHOST'), credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))

    # Set up the CSV file
    headers = None
    rows = []
    filename = 'data.csv'

    # Consume messages from the queue
    for method_frame, properties, body in channel.consume(os.getenv('RABBITMQ_QUEUE')):
        # Check if the message is empty, indicating that there are no more messages in the queue
        if body == None:
            break
        
        # Parse the JSON message
        message = json.loads(body.decode('utf-8'))

        # If this is the first message, save the headers
        if headers == None:
            headers = message.keys()
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

        # Append each item in preds to its own row in the CSV file
        for pred in message['data']['preds']:
            row = [message['device_id'], message['client_id'], message['created_at'], message['data']['license_id'], pred['image_frame'], pred['prob']]
            if pred['prob'] < 0.25:
                row.append('low_prob')
            else:
                row.append('')
            rows.append(row)
            with open(filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)

        # Acknowledge the message so it can be removed from the queue
        channel.basic_ack(method_frame.delivery_tag)

    # Stop consuming from the queue and close the connection
    channel.cancel()
    connection.close()

    # Return the CSV file as a JSON object
    response = {'headers': headers, 'rows': rows}
    return jsonify(response)
