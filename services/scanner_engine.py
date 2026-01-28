from datetime import datetime
from services.instrument_map import INSTRUMENT_MAP
from services.intraday_logic import intraday_boost_logic
from services.market_quote import get_market_quote


def breakout_logic():
    stocks = []

    for symbol in INSTRUMENT_MAP.keys():
        try:
            data = get_market_quote(symbol)

            ltp = data["ltp"]
            prev_close = data["prev_close"]

            percent = round(((ltp - prev_close) / prev_close) * 100, 2)

            # Breakout condition (only today's move)
            if percent > 1:
                stocks.append({
                    "symbol": symbol,
                    "ltp": ltp,
                    "percent": percent,
                    "signal": percent,
                    "time": datetime.now().strftime("%H:%M")
                })

        except:
            continue

    stocks.sort(key=lambda x: x["percent"], reverse=True)
    return stocks[:10]


def scan_all_stocks():
    breakout = breakout_logic()          # Today breakout logic
    intraday = intraday_boost_logic()   # Smart money SDK logic
    return breakout, intraday
