import json

def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)
