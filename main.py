from fastapi import FastAPI
from auth.routes import router as auth_router
from users.routes import router as users_router
from accounts.routes import router as accounts_router
from trades.routes import router as trades_router
from utils.json_db import JsonDB
from config import USERS_DB_PATH, ACCOUNTS_DB_PATH, TRADES_DB_PATH

app = FastAPI()

# Initialize JsonDB instances
users_db = JsonDB(USERS_DB_PATH)
accounts_db = JsonDB(ACCOUNTS_DB_PATH)
trades_db = JsonDB(TRADES_DB_PATH)

# Include routers
app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(users_router, prefix='/users', tags=['Users'])
app.include_router(accounts_router, prefix='/accounts', tags=['Accounts'])
app.include_router(trades_router, prefix='/trades', tags=['Trades'])

@app.get("/")
def root():
    return {"message": "Options Trading Platform"}
