## Scalable Image Inference API

This project is a Python-based scalable image inference API that uses a pre-trained object detection model YOLOv5 to perform inference on images.
The API is built using Flask, Celery for background task management, and Redis as a message broker.
It is containerized using Docker and designed to handle multiple concurrent requests efficiently.

Features :
*    RESTful API to accept image files and return object detection results.
*    Background task processing using Celery and Redis.
*    Supports concurrent request handling with scalable task queue management.
*    Object detection using YOLOv5 pre-trained model.
*    Dockerized for easy deployment and scalability.
### Table of Contents
## Requirements
## Installation
## Usage
Endpoints
Technologies
Architecture

#### Requirements
1. Python 3.9+
2. Docker & Docker Compose
3. Redis
