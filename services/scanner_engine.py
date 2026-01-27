from services.instrument_map import INSTRUMENT_MAP
from services.market_data import get_ltp, get_prev_day_data
from datetime import datetime
import pytz

ist = pytz.timezone('Asia/Kolkata')


def scan_all_stocks():
    breakout = []
    intraday = []

    for symbol, key in INSTRUMENT_MAP.items():
        ltp = get_ltp(key)
        prev = get_prev_day_data(key)  # yesterday high, close, volume

        if not prev:
            continue

        y_high = prev["high"]
        y_close = prev["close"]
        y_volume = prev["volume"]

        percent = round(((ltp - y_close) / y_close) * 100, 2)

        time_now = datetime.now(ist).strftime("%H:%M")

        stock = {
            "symbol": symbol,
            "ltp": ltp,
            "percent": percent,
            "signal": percent,
            "time": time_now
        }

        # ✅ BREAKOUT LOGIC
        if ltp > y_high:
            breakout.append(stock)

        # ✅ INTRADAY MOMENTUM LOGIC
        elif percent > 1:
            intraday.append(stock)

    # Top movers first
    breakout = sorted(breakout, key=lambda x: x["percent"], reverse=True)[:10]
    intraday = sorted(intraday, key=lambda x: x["percent"], reverse=True)[:10]

    return breakout, intraday
