from flask import Flask, request, jsonify
import pika
import json
import datetime

app = Flask(__name__)

@app.route('/predictions/', methods=['POST'])
def send_to_queue():
    # Get the JSON data from the request
    data = request.json
    print("printing data..................")
    print(data)
    # Validate the JSON data
    if not validate_data(data):
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    # Check the probability and add 'low_prob' tag if necessary
    for pred in data['data']['preds']:
        if pred['prob'] < 0.25 and 'low_prob' not in pred['tags']:
            pred['tags'].append('low_prob')
    
    # Add the timestamp to the message
    data['timestamp'] = str(datetime.datetime.now())
    
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='predictions')

    # Send the message to the queue
    channel.basic_publish(exchange='', routing_key='predictions', body=json.dumps(data))
    
    # Close the connection
    connection.close()

    return jsonify({'message': 'Message sent to the queue successfully.'}), 200

def validate_data(data):
    # Validate the JSON schema of the data here
    # Return True if data is valid, False otherwise
    if 'license_id' in data['data'] and 'preds' in data['data']:
       return True
    else:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
