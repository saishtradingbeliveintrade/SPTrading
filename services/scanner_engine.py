from services.market_data import get_ltp
from services.instrument_map import INSTRUMENT_MAP
from datetime import datetime
import random


def calculate_percent(ltp, prev_close):
    try:
        return round(((ltp - prev_close) / prev_close) * 100, 2)
    except:
        return 0


def generate_signal():
    return random.randint(40, 100)


def scan_all_stocks():
    breakout = []
    intraday = []

    for symbol in INSTRUMENT_MAP.keys():
        data = get_ltp(symbol)

        try:
            info = list(data["data"].values())[0]
            ltp = info["last_price"]

            # Dummy prev close (Upstox LTP API मध्ये नसतो)
            prev_close = ltp - random.uniform(-10, 10)

            percent = calculate_percent(ltp, prev_close)
            signal = generate_signal()
            time_now = datetime.now().strftime("%H:%M:%S")

            stock_obj = {
                "symbol": symbol,
                "ltp": round(ltp, 2),
                "percent": percent,
                "signal": signal,
                "time": time_now
            }

            if signal > 70:
                breakout.append(stock_obj)
            else:
                intraday.append(stock_obj)

        except:
            continue

    # Top 10 sort by signal
    breakout = sorted(breakout, key=lambda x: x["signal"], reverse=True)[:10]
    intraday = sorted(intraday, key=lambda x: x["signal"], reverse=True)[:10]

    return breakout, intraday
