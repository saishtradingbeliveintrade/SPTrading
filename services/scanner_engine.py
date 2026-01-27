import requests
from datetime import datetime
from config import UPSTOX_ACCESS_TOKEN
from services.instrument_map import INSTRUMENT_MAP

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}

QUOTE_URL = "https://api.upstox.com/v3/market-quote/quotes"


def get_quotes(keys: list):
    params = {"instrument_key": ",".join(keys)}
    r = requests.get(QUOTE_URL, headers=HEADERS, params=params)
    return r.json().get("data", {})


def percent_change(ltp, prev):
    if prev == 0:
        return 0
    return round(((ltp - prev) / prev) * 100, 2)


# ---------------- BREAKOUT LOGIC (UNCHANGED) ---------------- #
def breakout_score(pct, volume):
    score = 0
    score += abs(pct) * 2
    score += volume / 100000
    return score


# ---------------- INTRADAY SMART MONEY LOGIC ---------------- #
def intraday_score(pct, ltp, prev, volume, o, h, low):
    score = 0

    # Oversold bounce / reversal
    if pct < -1:
        score += 10

    # Strong move from low
    if (ltp - low) / low * 100 > 0.8:
        score += 15

    # Volume spike
    if volume > 500000:
        score += 20

    # Volatility range
    day_range = (h - low) / low * 100
    score += day_range

    # Recovery towards prev close
    recovery = (ltp - low) / (prev - low + 0.01)
    score += recovery * 10

    return round(score, 2)


def scan_all_stocks():
    symbols = list(INSTRUMENT_MAP.keys())
    keys = list(INSTRUMENT_MAP.values())

    data = get_quotes(keys)

    breakout_list = []
    intraday_list = []

    for sym, key in INSTRUMENT_MAP.items():
        stock = data.get(key)
        if not stock:
            continue

        ltp = stock["last_price"]
        prev = stock["prev_close"]
        volume = stock["volume"]
        o = stock["open"]
        h = stock["high"]
        low = stock["low"]

        pct = percent_change(ltp, prev)

        # -------- Breakout -------- #
        b_score = breakout_score(pct, volume)
        breakout_list.append({
            "symbol": sym,
            "ltp": ltp,
            "percent": pct,
            "signal": round(b_score, 2)
        })

        # -------- Intraday Boost -------- #
        i_score = intraday_score(pct, ltp, prev, volume, o, h, low)
        intraday_list.append({
            "symbol": sym,
            "ltp": ltp,
            "percent": pct,
            "signal": i_score
        })

    breakout_sorted = sorted(breakout_list, key=lambda x: x["signal"], reverse=True)[:10]
    intraday_sorted = sorted(intraday_list, key=lambda x: x["signal"], reverse=True)[:10]

    return breakout_sorted, intraday_sorted
