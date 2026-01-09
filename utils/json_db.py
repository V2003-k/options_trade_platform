import json
import os

def read_db(file_path: str):
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def write_db(file_path: str, data):
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)