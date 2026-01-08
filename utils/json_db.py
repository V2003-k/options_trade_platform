import json
import os

def read_db(file_path: str):
    """
    Read data from a JSON file.
    Returns empty dict if file does not exist or is invalid.
    """
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def write_db(file_path: str, data):
    """
    Write data to a JSON file.
    Creates directory if missing.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)