from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_utils import verify_token
from utils.json_db import JsonDB  # Import JsonDB here
from config import USERS_DB_PATH, ACCOUNTS_DB_PATH, TRADES_DB_PATH # Import paths from config

security = HTTPBearer()

# Initialize JsonDB instances at the module level in auth_dependency
users_db = JsonDB(USERS_DB_PATH)
accounts_db = JsonDB(ACCOUNTS_DB_PATH)
trades_db = JsonDB(TRADES_DB_PATH)

def get_db():
    return {"users": users_db, "accounts": accounts_db, "trades": trades_db}

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: dict = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload["user_id"]

    user = db["users"].find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": user["id"],
        "email": user["email"],
        "role": user.get("role", "user")
    }
