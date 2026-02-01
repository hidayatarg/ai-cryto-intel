from fastapi import FastAPI, Query
import requests

app = FastAPI(title="AI Crypto Market Intelligence")
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

@app.get("/health")
def health():
    return {"status": "ok"}


# Endpoint to get price summary of a cryptocurrency
# GET /price-summary?coin=solana
@app.get("/price-summary")
def price_summary(coin: str = Query(..., example="solana")):
    url = f"{COINGECKO_BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": coin,
        "price_change_percentage": "24h"
    }

    r = requests.get(url, params=params)
    data = r.json()

    if not data:
        return {"error": "Coin not found"}

    coin_data = data[0]

    print (coin_data)

    return {
        "coin": coin_data["id"],
        "price_usd": coin_data["current_price"],
        "change_24h_percent": coin_data["price_change_percentage_24h"],
        "market_cap": coin_data["market_cap"]
    }
