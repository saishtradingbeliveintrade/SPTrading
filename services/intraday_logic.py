from datetime import datetime
from services.instrument_map import INSTRUMENT_MAP
from services.upstox_sdk import quote_api, history_api


def get_live_quote(instrument):
    data = quote_api.get_full_market_quote(symbol=instrument)
    q = data.data[instrument]

    return {
        "ltp": q.last_price,
        "vwap": q.vwap,
        "high": q.ohlc.high,
        "low": q.ohlc.low,
        "volume": q.volume,
        "prev_close": q.ohlc.close
    }


def get_candles(instrument):
    candles = history_api.get_historical_candle_data1(
        instrument_key=instrument,
        interval="1minute",
        to_date=None,
        from_date=None
    )
    return candles.data.candles


def intraday_boost_logic():
    stocks = []

    for symbol, instrument in INSTRUMENT_MAP.items():
        try:
            quote = get_live_quote(instrument)
            candles = get_candles(instrument)

            ltp = quote["ltp"]
            vwap = quote["vwap"]
            volume = quote["volume"]
            prev_close = quote["prev_close"]

            percent = round(((ltp - prev_close) / prev_close) * 100, 2)

            # last 20 candles average volume
            avg_vol = sum([c[5] for c in candles[-20:]]) / 20

            volume_spike = volume > avg_vol * 2
            vwap_reclaim = ltp > vwap

            score = 0
            if volume_spike:
                score += 40
            if vwap_reclaim:
                score += 40
            if percent > -1:
                score += 20

            stocks.append({
                "symbol": symbol,
                "ltp": ltp,
                "percent": percent,
                "signal": score,
                "time": datetime.now().strftime("%H:%M")
            })

        except Exception:
            continue

    stocks.sort(key=lambda x: x["signal"], reverse=True)
    return stocks[:10]
