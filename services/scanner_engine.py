import os
import requests
from datetime import datetime
from services.instrument_map import INSTRUMENT_MAP

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

BREAKOUT_THRESHOLD = 1.2
INTRADAY_THRESHOLD = 0.8


def get_ltp_bulk():
    url = "https://api.upstox.com/v3/market-quote/ltp"
    params = {"instrument_key": ",".join(INSTRUMENT_MAP.values())}

    res = requests.get(url, headers=HEADERS, params=params, timeout=15)
    data = res.json().get("data", {})

    prices = {}
    for key, val in data.items():
        prices[key] = val["last_price"]

    return prices


def get_5min_candle(instrument_key):
    url = f"https://api.upstox.com/v3/historical-candle/intraday/{instrument_key}/minutes/5"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        candles = res.json()["data"]["candles"]
        return candles[-1] if candles else None
    except:
        return None


def get_day_open(instrument_key):
    url = f"https://api.upstox.com/v3/historical-candle/intraday/{instrument_key}/days/1"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        candles = res.json()["data"]["candles"]
        return candles[-1][1] if candles else None
    except:
        return None


def scan_market():
    breakout_list = []
    intraday_list = []

    print(f"Scanning {len(INSTRUMENT_MAP)} selected stocks...")

    ltp_prices = get_ltp_bulk()

    for symbol, key in INSTRUMENT_MAP.items():
        ltp = ltp_prices.get(key)
        if not ltp:
            continue

        open_price = get_day_open(key)
        candle = get_5min_candle(key)

        if not open_price or not candle:
            continue

        candle_open = candle[1]

        change_from_open = ((ltp - open_price) / open_price) * 100
        change_5min = ((ltp - candle_open) / candle_open) * 100

        entry = {
            "symbol": symbol,
            "ltp": round(ltp, 2),
            "%": round(change_from_open, 2),
            "signal%": round(change_5min, 2),
            "time": datetime.now().strftime("%H:%M:%S")
        }

        if change_5min > BREAKOUT_THRESHOLD:
            breakout_list.append(entry)

        if change_from_open > INTRADAY_THRESHOLD:
            intraday_list.append(entry)

    breakout_list.sort(key=lambda x: x["signal%"], reverse=True)
    intraday_list.sort(key=lambda x: x["%"], reverse=True)

    return breakout_list[:15], intraday_list[:15]
