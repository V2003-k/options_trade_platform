from fastapi import APIRouter, Depends, HTTPException, status
from utils.auth_dependency import get_current_user, get_db

router = APIRouter()

@router.get("/")
def list_accounts(current_user: dict = Depends(get_current_user), db: dict = Depends(get_db)):
    accounts = db["accounts"].find_all()
    user_accounts = [acc for acc in accounts if acc["user_id"] == current_user["id"]]
    return user_accounts

@router.get("/{account_id}")
def get_account_by_id(account_id: str, current_user: dict = Depends(get_current_user), db: dict = Depends(get_db)):
    account = db["accounts"].find_one({"id": account_id, "user_id": current_user["id"]})
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account
