# services/indicators.py

def percent_change(ltp, prev_close):
    return round(((ltp - prev_close) / prev_close) * 100, 2)


def volume_spike(current_vol, avg_vol):
    return current_vol > avg_vol * 1.8


def vwap_position(ltp, vwap):
    return ltp > vwap


def candle_strength(last_3_candles):
    # green candle count
    greens = sum(1 for c in last_3_candles if c['close'] > c['open'])
    return greens >= 2


def opening_range_break(ltp, orb_high, orb_low):
    if ltp > orb_high:
        return "UP"
    if ltp < orb_low:
        return "DOWN"
    return None
