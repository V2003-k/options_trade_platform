from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_utils import verify_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = verify_token(token)

    # return a normalized user object
    return {
        "user_id": payload["user_id"],
        "email": payload.get("email", "test@gmail.com"),
        "role": payload.get("role", "user")
    }