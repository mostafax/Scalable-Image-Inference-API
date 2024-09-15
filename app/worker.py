from celery import Celery
from utils.helpers import parse_results
import os
from model.model import ObjectDetectionModel
celery_app = Celery('worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@celery_app.task(name='worker.process_image_task')
def process_image_task(image_path):
    try:
        
        model = ObjectDetectionModel()
        results = model.predict(image_path)
        parsed_results = parse_results(results)
        return parsed_results
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    celery_app.start()
