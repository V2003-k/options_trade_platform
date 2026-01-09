import uuid
from utils.json_db import read_db, write_db
from config import DEMO_PRICES
from trades.pnl_calculation import calculate_pnl


def place_trade(user: dict, payload: dict):
    data = read_db("db/trades.json")
    
    if "trades" not in data:
        raise ValueError("No trades found")
    trade = {
        "trade_id": f"t-{uuid.uuid4().hex[:8]}",
        "account_id": payload["account_id"],
        "symbol": payload["symbol"],
        "side": payload["side"],
        "qty": payload["qty"],
        "trigger_price": payload["trigger_price"],
        "status": "placed"
    }

    data["trades"].append(trade)
    write_db("db/trades.json", data)
    return trade

def update_trade(user: dict, payload: dict):
    data = read_db("db/trades.json")

    for trade in data["trades"]:
        if trade["trade_id"] == payload["trade_id"]:
            trade["entry_price"] = DEMO_PRICES[trade["symbol"]]
            trade["status"] = "open"
            write_db("db/trades.json", data)
            return trade
        
    raise ValueError("Trade not found")

def close_trade(user: dict, payload: dict):
    data = read_db("db/trades.json")

    for trade in data["trades"]:
        if trade["trade_id"] == payload["trade_id"]:
            # demo price
            trade["exit_price"] = DEMO_PRICES[trade["symbol"]]

             #  PnL CALCULATION GOES HERE
            trade["pnl"] = calculate_pnl(
                trade["entry_price"],
                trade["exit_price"],
                trade["qty"],
                trade["side"]
            )
            trade["status"] = "closed"
            write_db("db/trades.json", data)
            return trade
        
    raise ValueError("Trade not found")