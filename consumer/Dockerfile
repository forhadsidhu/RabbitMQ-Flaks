FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY consumer.py consumer.py

VOLUME /app/csv


ENV CSV_FILE_PATH=/app/csv/data.csv

CMD ["python3", "consumer.py"]
