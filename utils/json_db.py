import json
import os
import uuid

class JsonDB:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the database file as an empty list if it doesn't exist or is invalid."""
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            self._write_data([])
        else:
            try:
                self._read_data()
            except json.JSONDecodeError:
                print(f"Warning: {self.file_path} is corrupted. Initializing with empty list.")
                self._write_data([])
            except Exception as e:
                print(f"Error initializing {self.file_path}: {e}")
                self._write_data([])

    def _read_data(self):
        """Reads all data from the JSON file."""
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Database file not found at {self.file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error: JSON decode error in {self.file_path}: {e}")
            # Attempt to recover by returning an empty list
            return []
        except Exception as e:
            print(f"Error reading data from {self.file_path}: {e}")
            return []

    def _write_data(self, data):
        """Writes data to a JSON file."""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error writing data to {self.file_path}: {e}")

    def find_all(self):
        """Returns all entries in the database."""
        return self._read_data()

    def find_one(self, query: dict):
        """Finds a single entry matching the query."""
        try:
            data = self._read_data()
            for item in data:
                if all(item.get(key) == value for key, value in query.items()):
                    return item
            return None
        except Exception as e:
            print(f"Error in find_one for {self.file_path}: {e}")
            return None

    def insert(self, new_entry: dict):
        """Inserts a new entry into the database."""
        try:
            data = self._read_data()
            if "id" not in new_entry:
                new_entry["id"] = str(uuid.uuid4())
            data.append(new_entry)
            self._write_data(data)
            return new_entry
        except Exception as e:
            print(f"Error in insert for {self.file_path}: {e}")
            raise # Re-raise to propagate the error

    def update(self, query: dict, updates: dict):
        """Updates entries matching the query."""
        try:
            data = self._read_data()
            updated_count = 0
            for i, item in enumerate(data):
                if all(item.get(key) == value for key, value in query.items()):
                    data[i].update(updates)
                    updated_count += 1
            self._write_data(data)
            return {"modified_count": updated_count}
        except Exception as e:
            print(f"Error in update for {self.file_path}: {e}")
            raise # Re-raise to propagate the error

    def delete(self, query: dict):
        """Deletes entries matching the query."""
        try:
            data = self._read_data()
            initial_len = len(data)
            data = [item for item in data if not all(item.get(key) == value for key, value in query.items())]
            self._write_data(data)
            return {"deleted_count": initial_len - len(data)}
        except Exception as e:
            print(f"Error in delete for {self.file_path}: {e}")
            raise # Re-raise to propagate the error
