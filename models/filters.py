NON_CRYPTO_KEYWORDS = [
    "gold", "oil", "stocks", "wall street",
    "fed", "interest rates", "inflation",
]

def is_crypto_relevant(title: str) -> bool:
    t = title.lower()
    return not any(k in t for k in NON_CRYPTO_KEYWORDS)