# Holds Storage stuff
import json
import os

MARRIAGE_FILE = "marriages.json"

def load_marriages():
    if not os.path.exists(MARRIAGE_FILE):
        return {}
    with open(MARRIAGE_FILE) as f:
        return json.load(f)


def save_marriages(data):
    with open(MARRIAGE_FILE, "w") as file:
        json.dump(data, file, indent=4)
        print(data)