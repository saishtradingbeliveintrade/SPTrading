# services/scorer.py

def calculate_score(params):
    score = 0

    if params["vol_spike"]:
        score += 20

    if params["above_vwap"]:
        score += 15

    if params["candle_strong"]:
        score += 15

    if params["orb"] == "UP":
        score += 25
    elif params["orb"] == "DOWN":
        score += 25

    if params["high_low_break"]:
        score += 15

    if params["relative_weak"]:
        score += 10

    return score  # out of 100
