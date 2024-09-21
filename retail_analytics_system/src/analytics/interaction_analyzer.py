import numpy as np

class InteractionAnalyzer:
    def __init__(self, config):
        self.pickup_sequence = config['pickup_sequence']
        self.putback_sequence = config['putback_sequence']

    def find_nearby_products(self, person_bbox, products):
        person_center = np.array([(person_bbox[0] + person_bbox[2]) / 2, (person_bbox[1] + person_bbox[3]) / 2])
        nearby_products = []
        for product_id, product in products.items():
            product_center = np.array([(product['bbox'][0] + product['bbox'][2]) / 2,
                                       (product['bbox'][1] + product['bbox'][3]) / 2])
            distance = np.linalg.norm(person_center - product_center)
            if distance < 100:  # Threshold for considering a product nearby
                nearby_products.append(product_id)
        return nearby_products

    def analyze(self, tracker_data):
        interactions = {}
        for customer_id, customer_data in tracker_data['customers'].items():
            sequence = customer_data['current_sequence']
            interactions[customer_id] = self.classify_interaction(sequence)
        return interactions

    def classify_interaction(self, sequence):
        gestures = [g for g, _ in sequence]
        if self.pickup_sequence == gestures[-len(self.pickup_sequence):]:
            return "pick_up"
        elif self.putback_sequence == gestures[-len(self.putback_sequence):]:
            return "put_back"
        elif "Reaching" in gestures[-3:] and not any(p for _, p in sequence[-3:]):
            return "confuse"
        return "none"