from fastapi import APIRouter, HTTPException, status, Depends
from auth.jwt_utils import create_access_token, verify_password, hash_password
from utils.auth_dependency import get_db
import uuid

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: dict, db: dict = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    if db["users"].find_one({"email": email}):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_password = hash_password(password)
    user_id = str(uuid.uuid4())

    new_user = {
        "id": user_id,
        "email": email,
        "hashed_password": hashed_password,
        "role": "user" # Default role
    }
    db["users"].insert(new_user)

    # Create a default paper trading account for the new user
    account_id = str(uuid.uuid4())
    new_account = {
        "id": account_id,
        "user_id": user_id,
        "account_type": "paper",
        "balance": 100000.0 # Initial demo balance
    }
    db["accounts"].insert(new_account)

    return {"message": "User registered successfully", "user_id": user_id}

@router.post("/login")
def login(data: dict, db: dict = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user = db["users"].find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["id"])
    return {"token": token, "type": "bearer"}
