import requests
from datetime import datetime
from config import UPSTOX_ACCESS_TOKEN
from services.instrument_map import INSTRUMENT_MAP

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}


def fetch_intraday_candles(key):
    url = f"https://api.upstox.com/v3/historical-candle/intraday/{key}/5minute"
    res = requests.get(url, headers=HEADERS)
    data = res.json()

    try:
        return data["data"]["candles"]
    except:
        return []


def calculate_vwap(candles):
    total_vol_price = 0
    total_vol = 0

    for c in candles:
        high, low, close, vol = c[2], c[3], c[4], c[5]
        avg_price = (high + low + close) / 3
        total_vol_price += avg_price * vol
        total_vol += vol

    return total_vol_price / total_vol if total_vol else 0


def score_stock(symbol, key):
    candles = fetch_intraday_candles(key)
    if len(candles) < 20:
        return None

    latest = candles[-1]
    prev = candles[-2]

    ltp = latest[4]
    prev_close = prev[4]

    percent = ((ltp - prev_close) / prev_close) * 100

    # --- VWAP ---
    vwap = calculate_vwap(candles[-20:])
    vwap_score = 20 if ltp > vwap else 0

    # --- Volume Spike ---
    avg_vol = sum([c[5] for c in candles[-10:-1]]) / 9
    vol_score = 20 if latest[5] > avg_vol * 1.8 else 0

    # --- Strong Candle ---
    body = abs(latest[4] - latest[1])
    range_candle = latest[2] - latest[3]
    candle_score = 20 if body > (range_candle * 0.6) else 0

    # --- High Break ---
    day_high = max([c[2] for c in candles[:-1]])
    high_score = 20 if ltp > day_high else 0

    # --- Momentum ---
    momentum_score = 20 if percent > 0.4 else 0

    total_score = vwap_score + vol_score + candle_score + high_score + momentum_score

    signal_percent = (total_score / 100) * 100

    return {
        "symbol": symbol,
        "ltp": round(ltp, 2),
        "percent": round(percent, 2),
        "signal": round(signal_percent, 2),
        "time": datetime.now().strftime("%H:%M")
    }


def scan_all_stocks():
    results = []

    for symbol, key in INSTRUMENT_MAP.items():
        data = score_stock(symbol, key)
        if data:
            results.append(data)

    # sort by signal strength
    results.sort(key=lambda x: x["signal"], reverse=True)

    breakout = results[:10]
    intraday = results[10:20]

    return breakout, intraday
