from datetime import datetime
from services.instrument_map import INSTRUMENT_MAP
from services.intraday_logic import intraday_boost_logic
from services.market_quote import get_market_quote   # तुझं आधीचं function

def breakout_logic():
    stocks = []

    for symbol, instrument in INSTRUMENT_MAP.items():
        try:
            data = get_market_quote(symbol)

            ltp = data["ltp"]
            prev_close = data["prev_close"]
            percent = round(((ltp - prev_close) / prev_close) * 100, 2)

            # simple breakout condition (तुझा जुना)
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
    breakout = breakout_logic()          # जुना logic
    intraday = intraday_boost_logic()   # SDK logic
    return breakout, intraday
