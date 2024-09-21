from collections import defaultdict
import datetime

class CustomerTracker:
    def __init__(self, config):
        self.customers = {}
        self.interaction_counts = defaultdict(lambda: {"pick_up": 0, "put_back": 0, "confuse": 0})
        self.interaction_threshold = config['interaction_threshold']

    def update(self, customer_id, gestures, nearby_products):
        if customer_id not in self.customers:
            self.customers[customer_id] = {
                'last_interaction': None,
                'current_sequence': []
            }

        customer = self.customers[customer_id]
        current_time = datetime.datetime.now()

        if customer['last_interaction'] is None or (current_time - customer['last_interaction']).total_seconds() > self.interaction_threshold:
            customer['current_sequence'] = []

        customer['current_sequence'].extend([(g, len(nearby_products) > 0) for g in gestures])
        customer['last_interaction'] = current_time

        self.analyze_sequence(customer_id, customer['current_sequence'])

    def analyze_sequence(self, customer_id, sequence):
        # Implement sequence analysis logic here
        pass

    def get_data(self):
        return {
            'customers': self.customers,
            'interaction_counts': dict(self.interaction_counts)
        }