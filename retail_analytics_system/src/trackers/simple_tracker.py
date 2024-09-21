import numpy as np

class SimpleTracker:
    def __init__(self):
        self.tracked_objects = {}
        self.next_id = 0

    def update(self, detections):
        new_tracked_objects = {}

        for detection in detections:
            bbox = detection[:4]
            confidence = detection[4]
            class_id = detection[5]

            if len(self.tracked_objects) > 0:
                distances = [np.linalg.norm(bbox[:2] - obj['bbox'][:2]) for obj in self.tracked_objects.values()]
                nearest_id = min(self.tracked_objects.keys(), key=lambda k: distances[k])

                if distances[nearest_id] < 50:  # Threshold for considering it the same object
                    new_tracked_objects[nearest_id] = {
                        'bbox': bbox,
                        'confidence': confidence,
                        'class_id': class_id
                    }
                    continue

            new_tracked_objects[self.next_id] = {
                'bbox': bbox,
                'confidence': confidence,
                'class_id': class_id
            }
            self.next_id += 1

        self.tracked_objects = new_tracked_objects
        return self.tracked_objects