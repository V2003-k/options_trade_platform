def calculate_pnl(entry_price: float, exit_price: float, qty: int, side: str) -> float:
    """
    BUY  -> (exit - entry) * qty
    SELL -> (entry - exit) * qty
    """
    if side.upper() == "BUY":
        return round((exit_price - entry_price) * qty, 2)

    elif side.upper() == "SELL":
        return round((entry_price - exit_price) * qty, 2)

    else:
        raise ValueError("Invalid trade side")

