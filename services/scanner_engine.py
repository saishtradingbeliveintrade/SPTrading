import requests
from datetime import datetime
from config import UPSTOX_ACCESS_TOKEN
from services.instrument_map import INSTRUMENT_MAP

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}


# ----------- BULK QUOTES (MAIN FIX) -----------
def fetch_bulk_quotes(keys: list):
    url = "https://api.upstox.com/v3/market-quote/quotes"
    joined = ",".join(keys)

    res = requests.get(
        url,
        headers=HEADERS,
        params={"instrument_key": joined}
    ).json()

    return res.get("data", {})


# ----------- COMMON CALC -----------
def percent_change(ltp, prev_close):
    if prev_close == 0:
        return 0
    return round(((ltp - prev_close) / prev_close) * 100, 2)


def now_time():
    return datetime.now().strftime("%H:%M")


# ----------- MAIN SCANNER -----------
def scan_all_stocks():
    breakout = []
    intraday = []

    all_keys = list(INSTRUMENT_MAP.values())
    quotes = fetch_bulk_quotes(all_keys)

    for symbol, key in INSTRUMENT_MAP.items():
        data = quotes.get(key)
        if not data:
            continue

        ltp = data["last_price"]
        prev_close = data["ohlc"]["close"]
        high = data["ohlc"]["high"]
        low = data["ohlc"]["low"]
        volume = data["volume"]

        pct = percent_change(ltp, prev_close)

        # ---------------- BREAKOUT LOGIC (today only) ----------------
        breakout_score = 0

        if ltp > high * 0.995:        # near day high
            breakout_score += 30
        if volume > 200000:          # raw spike check
            breakout_score += 20
        if pct > 1:
            breakout_score += 25
        if ltp > prev_close:
            breakout_score += 25

        if breakout_score >= 60:
            breakout.append({
                "symbol": symbol,
                "ltp": ltp,
                "percent": pct,
                "signal": breakout_score,
                "time": now_time()
            })

        # ---------------- INTRADAY BOOST (reversal / smart money) ----------------
        intraday_score = 0

        range_move = ((high - low) / prev_close) * 100

        if pct < 0 and ltp > (low + (high - low) * 0.4):
            intraday_score += 25      # recovery from low

        if range_move > 2:
            intraday_score += 20      # volatility

        if volume > 150000:
            intraday_score += 20      # activity

        if ltp > prev_close * 0.995:
            intraday_score += 20      # VWAP style reclaim approx

        if pct < -1:
            intraday_score += 15      # oversold bounce candidate

        if intraday_score >= 55:
            intraday.append({
                "symbol": symbol,
                "ltp": ltp,
                "percent": pct,
                "signal": intraday_score,
                "time": now_time()
            })

    # -------- SORT TOP 10 --------
    breakout = sorted(breakout, key=lambda x: x["signal"], reverse=True)[:10]
    intraday = sorted(intraday, key=lambda x: x["signal"], reverse=True)[:10]

    return breakout, intraday
