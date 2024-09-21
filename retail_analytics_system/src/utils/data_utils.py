import logging
import json
from pathlib import Path

class DataLogger:
    def __init__(self, config):
        log_file = Path(config['file'])
        log_file.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=str(log_file),
            level=getattr(logging, config['level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('RetailAnalytics')

    def log(self, data):
        self.logger.info(json.dumps(data))

def save_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)