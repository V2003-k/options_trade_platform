from fastapi import APIRouter, HTTPException
from auth.jwt_utils import create_access_token
from auth.password_utils import verify_password

router = APIRouter()

# temporary demo user
DEMO_USER = {
    "user_id": "USER123",
    "email": "test@gmail.com",
    "password": "123456"
}


@router.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if email != DEMO_USER["email"] or not verify_password(password, DEMO_USER["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(DEMO_USER["user_id"])
    return {"token": token}