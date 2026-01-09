from fastapi import APIRouter, HTTPException
from uuid import uuid4

from auth.jwt_utils import create_access_token
from auth.password_utils import verify_password
from auth.store_user import get_user_by_email, add_user

router = APIRouter()

@router.post("/signup")
def signup(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="User already exists")

    user = {
        "user_id": str(uuid4()),
        "email": email,
        "password": password  # plain for demo
    }

    add_user(user)
    return {"message": "User registered successfully"}


@router.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["user_id"])
    return {"token": token}