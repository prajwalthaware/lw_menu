import json
import os

DATA_FILE = '/var/www/data/travel_plan.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {'destinations': [], 'activities': [], 'accommodations': []}
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

