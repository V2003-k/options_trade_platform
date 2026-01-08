from fastapi import APIRouter, Depends
from utils.auth_dependency import get_current_user

router = APIRouter()

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user.get("role", "user")
    }