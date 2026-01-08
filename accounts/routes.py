from fastapi import APIRouter, Depends, HTTPException
from utils.auth_dependency import get_current_user
from utils.json_db import read_db, write_db
import uuid

router = APIRouter()

ACCOUNTS_FILE = "db/accounts.json"

@router.get("/")
def list_accounts(current_user: dict = Depends(get_current_user)):
    data = read_db(ACCOUNTS_FILE)

    accounts = data.get("accounts", [])

    return [
        acc for acc in accounts
        if acc["user_id"] == current_user["user_id"]
    ]


@router.post("/demo")
def create_demo_account(current_user: dict = Depends(get_current_user)):
    data = read_db(ACCOUNTS_FILE)

    if "accounts" not in data:
        data["accounts"] = []

    account = {
        "account_id": f"demo-{uuid.uuid4().hex[:6]}",
        "user_id": current_user["user_id"],
        "type": "demo",
        "balance": 100000,
        "currency": "USD"
    }

    data["accounts"].append(account)
    write_db(ACCOUNTS_FILE, data)

    return account