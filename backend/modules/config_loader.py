import json

def load_config(file_path: str) -> dict:
    with open(file_path, 'r', encoding="utf-8") as f:
        return json.load(f)
