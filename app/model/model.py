#MOCK model 

from ultralytics import YOLO

class ObjectDetectionModel:
    def __init__(self):
        self.model = YOLO("https://github.com/ultralytics/yolov5/releases/download/v6.2/yolov5s.pt")

    def predict(self, image_path):
        results = self.model(image_path)
        return results
