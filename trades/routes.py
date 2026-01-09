from fastapi import APIRouter, Depends, HTTPException, status
from utils.auth_dependency import get_current_user, get_db
from trades.trade_logic import place_trade, update_trade, close_trade

router = APIRouter()

@router.post("/place", status_code=status.HTTP_201_CREATED)
def place(payload: dict, current_user: dict = Depends(get_current_user), db: dict = Depends(get_db)):
    return place_trade(current_user, payload, db["users"], db["accounts"], db["trades"])

@router.put("/update/{trade_id}")
def update(trade_id: str, payload: dict, current_user: dict = Depends(get_current_user), db: dict = Depends(get_db)):
    payload["trade_id"] = trade_id # Add trade_id to payload for trade_logic
    return update_trade(current_user, payload, db["users"], db["accounts"], db["trades"])

@router.put("/close/{trade_id}")
def close(trade_id: str, current_user: dict = Depends(get_current_user), db: dict = Depends(get_db)):
    payload = {"trade_id": trade_id}
    return close_trade(current_user, payload, db["users"], db["accounts"], db["trades"])

@router.get("/")
def list_trades(current_user: dict = Depends(get_current_user), db: dict = Depends(get_db)):
    trades = db["trades"].find_all()
    user_trades = [trade for trade in trades if trade["user_id"] == current_user["id"]]
    return user_trades

@router.get("/{trade_id}")
def get_trade_by_id(trade_id: str, current_user: dict = Depends(get_current_user), db: dict = Depends(get_db)):
    trade = db["trades"].find_one({"id": trade_id, "user_id": current_user["id"]})
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trade not found or does not belong to user")
    return trade
