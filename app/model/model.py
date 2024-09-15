import torch
from ultralytics import YOLO

class ObjectDetectionModel:
    def __init__(self, weights_path=None):
        weights = weights_path if weights_path else "yolov5s.pt"
        
        # Check if GPU is available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load the model on the selected device (CPU or GPU)
        self.model = YOLO(weights).to(self.device)

    def predict(self, image_path):
        results = self.model(image_path, device=self.device)
        return results
