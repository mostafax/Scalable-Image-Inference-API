from celery import Celery
from model.model import ObjectDetectionModel
from utils.helpers import parse_results
import os

celery_app = Celery('worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

model = ObjectDetectionModel()

@celery_app.task(name='worker.process_image_task')
def process_image_task(image_path):
    try:
        results = model.predict(image_path)
        parsed_results = parse_results(results)
        os.remove(image_path)  # Optinal here we can do verious actions 
        return parsed_results
    except Exception as e:
        os.remove(image_path)
        return {'error': str(e)}
