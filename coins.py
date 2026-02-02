COIN_KEYWORDS = {
    "BTC": ["bitcoin", "btc", "satoshi"],
    "ETH": ["ethereum", "eth", "vitalik"],
    "SOL": ["solana", "sol"],
    "XRP": ["ripple", "xrp"],
}

# Coin extractor
def detect_coins(title: str) -> list[str]:
    title_l = title.lower()
    coins = []

    for coin, keywords in COIN_KEYWORDS.items():
        if any(k in title_l for k in keywords):
            coins.append(coin)

    return coins