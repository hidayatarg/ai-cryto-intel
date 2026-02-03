from collections import defaultdict

def aggregate_signals(signals: list) -> dict:
    """ Turns many news signals into per-coin trade bias """
    
    coin_stats = defaultdict(lambda: {
        "bullish": 0.0,
        "bearish": 0.0,
        "neutral": 0.0,
        "count": 0
    })

    for signal in signals:
        sentiment = signal["sentiment"]
        impact = signal["impact_score"]
        coins = signal["coins"]

        for coin in coins:
            coin_stats[coin][sentiment] += impact
            coin_stats[coin]["count"] += 1

    return build_trade_bias(coin_stats)


def build_trade_bias(coin_stats: dict) -> dict:
    results = {}
    MIN_SIGNALS = 2
    ACTION_THRESHOLD = 0.4
    for coin, stats in coin_stats.items():
        bull = stats["bullish"]
        bear = stats["bearish"]
        count = stats["count"]
        total = bull + bear + stats["neutral"]

        if total == 0:
            continue

        score = bull - bear

        if count < MIN_SIGNALS:
            action = "HOLD"
            confidence = 0.5

        else:
            if score >= ACTION_THRESHOLD:
                action = "BUY"
            elif score <= -ACTION_THRESHOLD:
                action = "SELL"
            else:
                action = "WATCH"

        

        confidence = min(abs(score) / total, 1.0)

        results[coin] = {
            "action": action,
            "confidence": round(confidence, 2),
            "bullish_score": round(bull, 2),
            "bearish_score": round(bear, 2),
            "signals": stats["count"]
        }

    return results
