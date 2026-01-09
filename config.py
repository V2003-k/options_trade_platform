
# JWT settings
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# Database paths
USERS_DB_PATH = "./db/users.json"
ACCOUNTS_DB_PATH = "./db/accounts.json"
TRADES_DB_PATH = "./db/trades.json"

# Demo prices for paper trading
DEMO_PRICES = {
    "AAPL": 150,
    "TSLA": 700,
    "INFY": 1450,
    "BTC": 42000
}