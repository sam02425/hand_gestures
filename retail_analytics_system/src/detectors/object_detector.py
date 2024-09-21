from ultralytics import YOLO
import numpy as np

class ObjectDetector:
    def __init__(self, config):
        self.model = YOLO(config['model_path'])
        self.confidence_threshold = config['confidence_threshold']
        self.person_class = config['person_class']
        self.product_classes = config['product_classes']

    def detect(self, frame):
        results = self.model(frame, conf=self.confidence_threshold)
        detections = results[0].boxes.data.cpu().numpy()

        persons = detections[detections[:, 5] == self.person_class]
        products = detections[np.isin(detections[:, 5], self.product_classes)]

        return persons, products