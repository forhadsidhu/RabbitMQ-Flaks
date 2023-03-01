# Multi-Container Service

This is a multi-container service that consists of a producer, a RabbitMQ queue, and a consumer. The producer is a simple web service that accepts a POST request with a JSON body, validates the body, parses and pushes the message to the RabbitMQ queue. The consumer reads from the RabbitMQ queue, transforms the message, and appends it into a CSV file.

## Requirements

- Docker
- docker-compose
- Python 3

## Installation

1. Clone the repository
2. Install requirements.txt
3. run the test.py file

