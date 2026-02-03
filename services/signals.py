from models.coins import detect_coins
from services.sentiment import analyze_sentiment

# Sentiment & Impact keywords
BULLISH_KEYWORDS = {
    "bullish", "surge", "rally", "breakout", "adoption",
    "partnership", "approval", "institutional", "record high",
     "soars", "breaks", "breaks out",
    "all-time high", "ath", "institutional inflows"
}

BEARISH_KEYWORDS = {
    "bearish", "hack", "exploit", "outage", "lawsuit",
    "sec", "ban", "collapse", "investigation", "downtime",
    "sell-off", "liquidation", "dump", "capitulation"
}

HIGH_IMPACT_KEYWORDS = {
    "sec", "hack", "exploit", "lawsuit", "etf",
    "bankruptcy", "investigation", "regulation"
}

# MEDIUM_IMPACT_KEYWORDS = {
#     "adoption", "partnership", "approval", "institutional",
#     "rally", "surge", "breakout", "record high", "downtime"
# }

# Text normalization
def normalize(text: str) -> str:
    return text.lower().strip()

# Sentiment scoring engine
def extract_signal(title: str) -> dict:
    sentiment, impact = analyze_sentiment(title)

    coins = detect_coins(title)

    return {
        "sentiment": sentiment,
        "impact_score": impact,
        "coins": coins,
        "is_relevant": bool(coins),
    }