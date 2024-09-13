#MOCK model 

import torch

class ObjectDetectionModel:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    def predict(self, image_path):
        results = self.model(image_path)
        return results
