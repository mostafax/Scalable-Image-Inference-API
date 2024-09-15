#MOCK model 

import torch
from ultralytics import YOLO
import os

class ObjectDetectionModel:
    def __init__(self):
        local_weights_path = 'weights/yolov5s.pt'
        if os.path.exists(local_weights_path):
            self.model = YOLO(local_weights_path)
        else:
            self.model = YOLO("https://github.com/ultralytics/yolov5/releases/download/v6.2/yolov5s.pt")

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

    def predict(self, image_path):
        results = self.model(image_path, device=self.device)
        return results
