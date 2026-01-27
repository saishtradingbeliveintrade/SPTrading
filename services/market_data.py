import requests
from datetime import datetime
from config import UPSTOX_ACCESS_TOKEN
from services.instrument_map import INSTRUMENT_MAP

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}

# time store (breakout trigger time freeze)
TRIGGER_TIME = {}


def get_ltp(symbol: str):
    key = INSTRUMENT_MAP.get(symbol.upper())

    if not key:
        return {"error": "Invalid symbol"}

    # ✅ QUOTES API (gives prev close)
    url = f"https://api.upstox.com/v3/market-quote/quotes?instrument_key={key}"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def process_stock(symbol: str):
    data = get_ltp(symbol)

    try:
        item = list(data["data"].values())[0]

        ltp = item["last_price"]
        prev_close = item["ohlc"]["close"]
        volume = item.get("volume", 0)

        # ✅ % Change
        pct = round(((ltp - prev_close) / prev_close) * 100, 2)

        # ---------------- SIGNAL LOGIC ----------------
        signal_score = 0

        # Volume spike basic
        if volume > 500000:
            signal_score += 20

        # Price above prev close
        if ltp > prev_close:
            signal_score += 20

        # Strong move
        if pct > 1:
            signal_score += 20

        # Big move
        if pct > 2:
            signal_score += 20

        # Extra momentum
        if pct > 3:
            signal_score += 20

        signal_pct = min(signal_score, 100)

        # -------- Trigger Time Freeze --------
        if signal_pct >= 60 and symbol not in TRIGGER_TIME:
            TRIGGER_TIME[symbol] = datetime.now().strftime("%H:%M")

        trigger_time = TRIGGER_TIME.get(symbol, "-")

        return {
            "symbol": symbol,
            "price": ltp,
            "pct": pct,
            "signal_pct": signal_pct,
            "time": trigger_time
        }

    except Exception as e:
        return {
            "symbol": symbol,
            "price": 0,
            "pct": 0,
            "signal_pct": 0,
            "time": "-"
        }


def get_multiple_processed(symbols: list):
    results = []

    for sym in symbols:
        results.append(process_stock(sym))

    # sort by signal strength
    results = sorted(results, key=lambda x: x["signal_pct"], reverse=True)

    return results[:10]
