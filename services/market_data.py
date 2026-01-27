import requests
from datetime import datetime
from config import UPSTOX_ACCESS_TOKEN
from services.instrument_map import INSTRUMENT_MAP

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}

# 👉 signal time freeze store
signal_times = {}


# ---------- BASIC CALC ----------
def percent_change(ltp, prev_close):
    try:
        return round(((ltp - prev_close) / prev_close) * 100, 2)
    except:
        return 0


def get_signal_time(symbol):
    return signal_times.get(symbol)


def set_signal_time(symbol):
    if symbol not in signal_times:
        signal_times[symbol] = datetime.now().strftime("%H:%M")


# ---------- LTP API ----------
def get_ltp(symbol: str):
    key = INSTRUMENT_MAP.get(symbol.upper())

    if not key:
        return {"error": "Invalid symbol"}

    url = f"https://api.upstox.com/v3/market-quote/quotes?instrument_key={key}"
    res = requests.get(url, headers=HEADERS)
    return res.json()


# ---------- PROCESS STOCK (logic layer) ----------
def process_stock(sym, data):
    try:
        item = list(data["data"].values())[0]

ltp = item["last_price"]
prev_close = item["ohlc"]["close"]
        pct = percent_change(ltp, prev_close)

        # 🔥 temporary signal score logic (next step मध्ये real indicators)
        signal_pct = abs(pct) * 5
        signal_pct = min(round(signal_pct, 2), 100)

        # signal trigger condition
        if signal_pct > 20:
            set_signal_time(sym)

        time = get_signal_time(sym)

        return {
            "symbol": sym,
            "price": ltp,
            "pct": pct,
            "signal_pct": signal_pct,
            "time": time
        }

    except:
        return {
            "symbol": sym,
            "price": "Error",
            "pct": 0,
            "signal_pct": 0,
            "time": None
        }


# ---------- MULTIPLE LTP WITH LOGIC ----------
def get_multiple_ltp(symbols: list):
    processed = []

    for sym in symbols:
        raw = get_ltp(sym)
        stock = process_stock(sym, raw)
        processed.append(stock)

    # 🔥 sorting by signal strength
    processed.sort(key=lambda x: x["signal_pct"], reverse=True)

    return processed
