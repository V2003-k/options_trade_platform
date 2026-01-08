from fastapi import Request, HTTPException
from auth.jwt_utils import verify_token

def jwt_middleware(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token = auth_header.split(" ")[1]  # Bearer <token>
        payload = verify_token(token)
        request.state.user_id = payload["user_id"]
        return payload
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")