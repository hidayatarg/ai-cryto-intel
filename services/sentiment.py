def analyze_sentiment(title: str):
    if not title:
        return "neutral", 0.0

    text = title.lower()

    bullish_keywords = {
        "surge": 0.4,
        "rally": 0.4,
        "breakout": 0.5,
        "bullish": 0.4,
        "pump": 0.3,
        "record high": 0.6,
        "adoption": 0.4,
        "approval": 0.5,
        "win": 0.3,
        "growth": 0.3,
        "institutional": 0.4,
        "etf": 0.4,
        "inflow": 0.3
    }

    bearish_keywords = {
        "crash": -0.6,
        "dump": -0.4,
        "slip": -0.3,
        "drop": -0.3,
        "selloff": -0.5,
        "bearish": -0.4,
        "collapse": -0.6,
        "ban": -0.5,
        "lawsuit": -0.4,
        "hack": -0.6,
        "investigation": -0.5,
        "powering down": -0.4,
        "plunge": -0.5,
        "liquidation": -0.6
    }

    score = 0.0

    for word, weight in bullish_keywords.items():
        if word in text:
            score += weight

    for word, weight in bearish_keywords.items():
        if word in text:
            score += weight

    if score > 0.15:
        sentiment = "bullish"
    elif score < -0.15:
        sentiment = "bearish"
    else:
        sentiment = "neutral"

    impact_score = min(abs(score), 1.0)

    return sentiment, round(impact_score, 2)
