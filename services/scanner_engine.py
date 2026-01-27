import requests
from datetime import datetime
from config import UPSTOX_ACCESS_TOKEN
from services.instrument_map import INSTRUMENT_MAP

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}


def fetch_intraday_candles(instrument_key):
    url = f"https://api.upstox.com/v3/historical-candle/intraday/{instrument_key}/minutes/5"
    res = requests.get(url, headers=HEADERS).json()

    try:
        return res["data"]["candles"]
    except:
        return []


def score_stock(symbol, instrument_key):
    candles = fetch_intraday_candles(instrument_key)

    if len(candles) < 20:
        return None

    closes = [c[4] for c in candles]
    volumes = [c[5] for c in candles]

    last_price = closes[-1]
    prev_price = closes[-10]

    price_move = ((last_price - prev_price) / prev_price) * 100

    avg_vol = sum(volumes[:-1]) / len(volumes[:-1])
    vol_spike = volumes[-1] > 2 * avg_vol

    score = 0
    if price_move > 0.8:
        score += 50
    if vol_spike:
        score += 50

    if score < 50:
        return None

    return {
        "symbol": symbol,
        "ltp": round(last_price, 2),
        "percent": round(price_move, 2),
        "signal": round(price_move, 2),
        "time": datetime.now().strftime("%H:%M"),
        "score": score
    }


def scan_all_stocks():
    results = []

    for symbol, key in INSTRUMENT_MAP.items():
        data = score_stock(symbol, key)
        if data:
            results.append(data)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:10], results[10:20]
