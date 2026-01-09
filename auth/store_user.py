import json
from pathlib import Path

USER_FILE = Path("db/users.json")

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)["users"]


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump({"users": users}, f, indent=2)


def get_user_by_email(email: str):
    users = load_users()
    for user in users:
        if user["email"] == email:
            return user
    return None


def add_user(user: dict):
    users = load_users()
    users.append(user)
    save_users(users)