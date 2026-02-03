import os
from fastapi import FastAPI, Query
import requests
from dotenv import load_dotenv
from services.signals import extract_signal
from services.aggregator import aggregate_signals

load_dotenv()

app = FastAPI(title="AI Crypto Market Intelligence")
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
CRYPTOPANIC_BASE = "https://cryptopanic.com/api/developer/v2/posts/"
CRYPTOPANIC_KEY = os.getenv("CRYPTOPANIC_API_KEY")

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

    return {
        "coin": coin_data["id"],
        "price_usd": coin_data["current_price"],
        "change_24h_percent": coin_data["price_change_percentage_24h"],
        "market_cap": coin_data["market_cap"]
    }

# Endpoint to get latest news articles about cryptocurrencies
# GET /news ==> return raw news data
@app.get("/news")
def crypto_news(limit: int = 10):
    if not CRYPTOPANIC_KEY:
        raise HTTPException(status_code=500, detail="Missing CryptoPanic API key")

    params = {
        "auth_token": CRYPTOPANIC_KEY,
        "public": "true"
    }

    r = requests.get(
        CRYPTOPANIC_BASE,
        params=params,
        headers={"Accept": "application/json"}
    )

    if r.status_code != 200:
        return {
            "error": "CryptoPanic API error",
            "status_code": r.status_code,
            "response": r.text[:300]
        }

    data = r.json()

    return [
        {
            "title": item.get("title"),
            "url": item.get("url"),
            "kind": item.get("kind") or "CryptoPanic.com",
            "published_at": item.get("published_at"),
            "created_at": item.get("created_at")
        }
        for item in data.get("results", [])
    ]

# Endpoint to analyze news signals
# GET /news-signals ===> return filtered inteligence with sentiment & impact
@app.get("/news-signals")
def news_signals():
    if not CRYPTOPANIC_KEY:
        raise HTTPException(status_code=500, detail="Missing CryptoPanic API key")

    params = {
        "auth_token": CRYPTOPANIC_KEY,
        "public": "true"
    }

    r = requests.get(CRYPTOPANIC_BASE, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()
    results = []

    for item in data.get("results", []):
        title = item.get("title", "")

        signal = extract_signal(title)

        # Noise filter
        if signal["impact_score"] < 0.2:
            continue

        results.append({
            "title": title,
            "sentiment": signal["sentiment"],
            "impact_score": signal["impact_score"],
            "coins": signal["coins"],
        })

    results = sorted(results, key=lambda x: x["impact_score"], reverse=True)
    return results

# Endpoint to get aggregated trade bias from news signals
# GET /trade-signals ===> return actionable decision
@app.get("/trade-signals")
def trade_signals():
    if not CRYPTOPANIC_KEY:
        raise HTTPException(status_code=500, detail="Missing CryptoPanic API key")
    
    params = {
        "auth_token": CRYPTOPANIC_KEY,
        "public": "true"
    }

    r = requests.get(CRYPTOPANIC_BASE, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()
    signals = []

    for item in data.get("results", []):
        title = item.get("title", "")

        signal = extract_signal(title)

        # Noise filter
        if signal["impact_score"] < 0.2:
            continue

        # Relevance filter
        if not signal["coins"]:
            continue

        signals.append(signal)

    return aggregate_signals(signals)