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
def extract_signal(title: str, description: str):
    text = normalize(f"{title} {description}")

    bullish_hits = sum(1 for k in BULLISH_KEYWORDS if k in text)
    bearish_hits = sum(1 for k in BEARISH_KEYWORDS if k in text)
    impact_hits = sum(1 for k in HIGH_IMPACT_KEYWORDS if k in text)

    if bullish_hits > bearish_hits:
        sentiment = "bullish"
    elif bearish_hits > bullish_hits:
        sentiment = "bearish"
    else:
        sentiment = "neutral"

    impact_score = min(
        1.0,
        impact_hits * 0.4 + abs(bullish_hits - bearish_hits) * 0.2
    )

    return {
        "sentiment": sentiment,
        "impact_score": round(impact_score, 2),
        "bullish_hits": bullish_hits,
        "bearish_hits": bearish_hits
    }