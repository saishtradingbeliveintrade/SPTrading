import requests
from datetime import datetime
from config import UPSTOX_ACCESS_TOKEN
from services.instrument_map import INSTRUMENT_MAP

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}

TRIGGER_TIME = {}


def fetch_quote(key):
    url = f"https://api.upstox.com/v3/market-quote/quotes?instrument_key={key}"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def process_stock(symbol, key):
    try:
        data = fetch_quote(key)
        item = list(data["data"].values())[0]

        ltp = item["last_price"]
        prev_close = item["ohlc"]["close"]
        volume = item.get("volume", 0)

        pct = round(((ltp - prev_close) / prev_close) * 100, 2)

        # -------- BASIC SCORING --------
        score = 0

        if volume > 300000:
            score += 20
        if pct > 1:
            score += 20
        if pct > 2:
            score += 20
        if pct > 3:
            score += 20
        if ltp > prev_close:
            score += 20

        signal = min(score, 100)

        if signal >= 60 and symbol not in TRIGGER_TIME:
            TRIGGER_TIME[symbol] = datetime.now().strftime("%H:%M")

        time = TRIGGER_TIME.get(symbol, "-")

        return {
            "symbol": symbol,
            "ltp": ltp,
            "pct": pct,
            "signal": signal,
            "time": time
        }

    except:
        return None


def scan_all_stocks():
    results = []

    for symbol, key in INSTRUMENT_MAP.items():
        stock = process_stock(symbol, key)
        if stock:
            results.append(stock)

    # sort by signal strength
    results = sorted(results, key=lambda x: x["signal"], reverse=True)

    # top 20
    top20 = results[:20]

    breakout = top20[:10]
    intraday = top20[10:20]

    return breakout, intraday
# --- compatibility function for api route ---
def get_ltp(symbol: str):
    key = INSTRUMENT_MAP.get(symbol.upper())
    if not key:
        return {"error": "Invalid symbol"}

    data = fetch_quote(key)
    return data
import requests
import os

TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

def get_prev_day_data(instrument_key):
    url = f"https://api.upstox.com/v3/historical-candle/{instrument_key}/days/1"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    r = requests.get(url, headers=headers).json()

    try:
        candle = r["data"]["candles"][0]
        return {
            "high": candle[2],
            "close": candle[4],
            "volume": candle[5],
        }
    except:
        return None
