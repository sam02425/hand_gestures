import yaml
from pathlib import Path
import cv2
from src.detectors.object_detector import ObjectDetector
from src.detectors.gesture_detector import GestureDetector
from src.trackers.customer_tracker import CustomerTracker
from src.trackers.simple_tracker import SimpleTracker
from src.analytics.interaction_analyzer import InteractionAnalyzer
from src.utils.video_utils import VideoStream
from src.utils.data_utils import DataLogger

class RetailAnalyticsSystem:
    def __init__(self, config_path):
        with open(config_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

        self.object_detector = ObjectDetector(self.config['object_detection'])
        self.gesture_detector = GestureDetector(self.config['gesture_detection'])
        self.customer_tracker = CustomerTracker(self.config['customer_tracking'])
        self.person_tracker = SimpleTracker()
        self.product_tracker = SimpleTracker()
        self.interaction_analyzer = InteractionAnalyzer(self.config['analytics'])
        self.video_stream = VideoStream(self.config['video'])
        self.data_logger = DataLogger(self.config['logging'])

    def run(self):
        while True:
            frame = self.video_stream.read()
            if frame is None:
                break

            persons, products = self.object_detector.detect(frame)
            tracked_persons = self.person_tracker.update(persons)
            tracked_products = self.product_tracker.update(products)

            hand_landmarks = self.gesture_detector.detect(frame)

            for person_id, person in tracked_persons.items():
                gestures = self.gesture_detector.classify_gestures(hand_landmarks, person['bbox'])
                nearby_products = self.interaction_analyzer.find_nearby_products(person['bbox'], tracked_products)
                self.customer_tracker.update(person_id, gestures, nearby_products)

            interactions = self.interaction_analyzer.analyze(self.customer_tracker.get_data())
            self.data_logger.log(interactions)

            self.visualize_results(frame, tracked_persons, tracked_products, interactions)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_stream.release()
        cv2.destroyAllWindows()

    def visualize_results(self, frame, persons, products, interactions):
        # Implement visualization logic here
        pass

if __name__ == "__main__":
    config_path = Path("config/config.yaml")
    system = RetailAnalyticsSystem(config_path)
    system.run()