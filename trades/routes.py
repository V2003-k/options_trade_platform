from fastapi import APIRouter, Depends
from utils.auth_dependency import get_current_user
from trades.trade_logic import place_trade, update_trade, close_trade
from utils.json_db import read_db

router = APIRouter()

@router.get("/")
def list_trades(current_user: dict = Depends(get_current_user)):
    data = read_db("db/trades.json")
    return data["trades"]

@router.post("/place")
def place(payload: dict, current_user: dict = Depends(get_current_user)):
    return place_trade(current_user, payload)

@router.post("/update")
def update(payload: dict, current_user: dict = Depends(get_current_user)):
    return update_trade(current_user, payload)

@router.post("/close")
def close(payload: dict, current_user: dict = Depends(get_current_user)):
    return close_trade(current_user, payload)