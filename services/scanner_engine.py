import requests
from datetime import datetime
from config import UPSTOX_ACCESS_TOKEN
from services.instrument_map import INSTRUMENT_MAP

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}

# ---------------- LTP ----------------
def get_ltp(symbol):
    key = INSTRUMENT_MAP.get(symbol.upper())
    url = f"https://api.upstox.com/v3/market-quote/ltp?instrument_key={key}"
    res = requests.get(url, headers=HEADERS).json()
    return list(res["data"].values())[0]["last_price"]


# ---------------- CANDLES (CORRECT API) ----------------
def fetch_intraday_candles(symbol):
    url = f"https://api.upstox.com/v3/historical-candle/intraday/NSE_EQ/{symbol}/minutes/5"
    res = requests.get(url, headers=HEADERS).json()

    try:
        return res["data"]["candles"]
    except:
        return []


# ---------------- SCORING LOGIC ----------------
def score_stock(symbol):
    candles = fetch_intraday_candles(symbol)

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
        score += 40
    if vol_spike:
        score += 40

    if score < 40:
        return None

    signal_pct = round(price_move, 2)
    signal_time = datetime.now().strftime("%H:%M")

    return {
        "symbol": symbol,
        "ltp": round(last_price, 2),
        "percent": round(price_move, 2),
        "signal": signal_pct,
        "time": signal_time,
        "score": score
    }


# ---------------- MAIN SCANNER ----------------
def scan_all_stocks():
    results = []

    for symbol in INSTRUMENT_MAP.keys():
        data = score_stock(symbol)
        if data:
            results.append(data)

    # sort by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    breakout = results[:10]
    intraday = results[10:20]

    return breakout, intraday
