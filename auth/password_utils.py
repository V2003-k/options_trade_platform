def verify_password(plain_password: str, stored_password: str) -> bool:
    # simple comparison for demo
    return plain_password == stored_password