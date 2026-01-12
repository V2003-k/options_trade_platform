import uuid
from datetime import datetime
from config import DEMO_PRICES
from trades.pnl_calculation import calculate_pnl
from fastapi import HTTPException, status

def place_trade(user: dict, payload: dict, users_db, accounts_db, trades_db):
    try:
        account_id = payload["account_id"]
        symbol = payload["symbol"].upper()
        side = payload["side"].upper() # BUY or SELL
        qty = payload["quantity"]
        trigger_price = payload["trigger_point"]

        # --- DEBUG PRINTS START ---
        print(f"DEBUG: Current User ID from token: {user['id']}")
        print(f"DEBUG: Account ID received in payload: {account_id}")
        # --- DEBUG PRINTS END ---

        # Validate account ownership
        account = accounts_db.find_one({"id": account_id, "user_id": user["id"]})
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found or does not belong to user")

        if symbol not in DEMO_PRICES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid symbol: {symbol}")

        current_price = DEMO_PRICES[symbol]

        # Basic balance check for BUY orders
        if side == "BUY":
            cost = qty * current_price
            if account["balance"] < cost:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
            account["balance"] -= cost
            # Track shares for BUY (optional, for paper trading)
            account.setdefault("positions", {})
            account["positions"].setdefault(symbol, 0)
            account["positions"][symbol] += qty
        elif side == "SELL":
            # Check if user has enough shares to sell
            account.setdefault("positions", {})
            account["positions"].setdefault(symbol, 0)
            if account["positions"][symbol] < qty:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient shares to sell")
            account["positions"][symbol] -= qty
            # Add proceeds to balance
            proceeds = qty * current_price
            account["balance"] += proceeds
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid trade side. Must be BUY or SELL")

        trade = {
            "id": str(uuid.uuid4()),
            "user_id": user["id"],
            "account_id": account_id,
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "trigger_price": trigger_price,
            "entry_price": current_price, # Placed price is the current demo price
            "status": "placed",
            "timestamp": datetime.utcnow().isoformat()
        }

        trades_db.insert(trade)
        accounts_db.update({"id": account_id}, {"balance": account["balance"], "positions": account["positions"]})

        return trade
    except Exception as e:
        print(f"Error in place_trade: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")

def update_trade(user: dict, payload: dict, users_db, accounts_db, trades_db):
    trade_id = payload["trade_id"]
    entry_point = payload.get("entry_point")

    trade = trades_db.find_one({"id": trade_id, "user_id": user["id"]})
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trade not found or does not belong to user")

    if trade["status"] != "placed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only placed trades can be updated")

    # For simplicity, 'entry_point' is hardcoded to current demo price as per requirements
    # In a real app, this would be the actual execution price
    trade["entry_price"] = DEMO_PRICES[trade["symbol"]]
    trade["status"] = "open" # Change status to open after entry point is set
    trade["entry_point"] = entry_point # Store the entry_point given by user

    trades_db.update({"id": trade_id}, {"entry_price": trade["entry_price"], "status": "open", "entry_point": entry_point})
    return trade

def close_trade(user: dict, payload: dict, users_db, accounts_db, trades_db):
    trade_id = payload["trade_id"]
    exit_price = payload.get("exit_price")

    trade = trades_db.find_one({"id": trade_id, "user_id": user["id"]})
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trade not found or does not belong to user")

    if trade["status"] != "open":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only open trades can be closed")

    # Use exit_price from payload if provided, else fallback to demo price
    if exit_price is None:
        exit_price = DEMO_PRICES[trade["symbol"]]

    pnl = calculate_pnl(
        trade["entry_price"],
        float(exit_price),
        trade["qty"],
        trade["side"]
    )

    # Update account balance with PnL
    account = accounts_db.find_one({"id": trade["account_id"]})
    if account:
        account["balance"] += pnl
        accounts_db.update({"id": account["id"]}, {"balance": account["balance"]})

    trade["exit_price"] = float(exit_price)
    trade["pnl"] = pnl
    trade["status"] = "closed"
    trade["closed_timestamp"] = datetime.utcnow().isoformat()

    trades_db.update({"id": trade_id}, {"exit_price": float(exit_price), "pnl": pnl, "status": "closed", "closed_timestamp": trade["closed_timestamp"]})
    return trade
