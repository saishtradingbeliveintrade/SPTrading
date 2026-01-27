import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

# 👉 तुझं 200 stock instrument map
from services.instrument_map import INSTRUMENT_MAP


ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")


def get_ist_time():
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M")


def get_ltp(instrument_key):
    url = "https://api.upstox.com/v2/market-quote/ltp"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }
    params = {"instrument_key": instrument_key}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        data = r.json()

        if "data" in data and instrument_key in data["data"]:
            return data["data"][instrument_key]["last_price"]
    except Exception:
        pass

    return None


def scan_all_stocks():
    breakout = []
    intraday = []

    for symbol, instrument_key in INSTRUMENT_MAP.items():
        ltp = get_ltp(instrument_key)
        if not ltp:
            continue

        # Dummy math (तू पुढे logic बदलू शकतोस)
        percent = round((ltp % 5) - 2.5, 2)
        signal = percent

        stock_data = {
            "symbol": symbol,
            "ltp": ltp,
            "percent": percent,
            "signal": signal,
            "time": get_ist_time()
        }

        # Same logic दोन्हीकडे लागू होईल
        if percent >= 1:
            breakout.append(stock_data)
        else:
            intraday.append(stock_data)

    # Top 10 only
    breakout = sorted(breakout, key=lambda x: -x["percent"])[:10]
    intraday = sorted(intraday, key=lambda x: -x["percent"])[:10]

    return breakout, intraday
