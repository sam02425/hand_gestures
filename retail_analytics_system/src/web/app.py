from flask import Flask, render_template, jsonify
from src.utils.data_utils import load_json
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/interactions')
def get_interactions():
    data_file = Path('data/processed/interactions.json')
    if data_file.exists():
        data = load_json(data_file)
        return jsonify(data)
    else:
        return jsonify({'error': 'No data available'}), 404

def start_web_server(host, port):
    app.run(host=host, port=port)