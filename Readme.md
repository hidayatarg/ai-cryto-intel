# AI Crypto Intels
A project to build an AI-powered cryptocurrency intelligence platform using FastAPI.
## Data Collection
### 1. Install Dependencies
- Python
- FastAPI
- Uvicorn 
- Requests
### 2. Integrate CoinGecko API 
Collecting real-time cryptocurrency data from CoinGecko API.
### 3. Integrate CryptoPanic API
Pull real-time crypto news, normalize it, and expose it via API.
- Store headlines + timestamps
- Basic filtering (bullish / bearish)
- Market Sentiments

Require API Key from CryptoPanic.com

## Thinking Layer
### 4. Implementing First LLM Call
In this step we do the Signal Extraction, we will use a simple keyword matching approach to classify news headlines as bullish or bearish.
We convert news to signals.

### 5. Improve Signal Quality
We improve the signal quality, added a sentiment score.

### 6. Signal Aggregation & Trade Bias Engine
Aggregate signals over time to generate trade bias (buy/sell/hold).
For each coin:
- Count bullish vs bearish signals
- Weight by impact score
- Decide a trade bias
