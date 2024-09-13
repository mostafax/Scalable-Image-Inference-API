# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY ./app /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
