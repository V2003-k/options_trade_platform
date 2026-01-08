from fastapi import APIRouter, Depends
from utils.auth_dependency import get_current_user
from utils.json_db import read_db, write_db
import uuid

router = APIRouter()

@router.get("/")
def list_accounts(curretn_user: dict = Depends(get_current_user)):
    data = read_db("accounts.json")
    return [
        acc for acc in data['accounts']
        if acc['user_id'] == curretn_user['user_id']
    ]

@router.post("/demo")
def create_demo_account(current_user: dict = Depends(get_current_user)):
    data = read_db("accoutns.json")
    
    account = {
        "account_id": f"demo-{uuid.uuid4().hex[:6]}",
        "user_id": current_user["user_id"],
        "type": "demo",
        "balance": 100000,
        "currency": "USD"
    }

    data["accounts"].append(account)
    write_db("accounts.json", data)

    return account