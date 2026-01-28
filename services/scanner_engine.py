from services.breakout_logic import breakout_logic
from services.intraday_logic import intraday_boost_logic


def scan_all_stocks():
    breakout = breakout_logic()          # तुझा जुना logic
    intraday = intraday_boost_logic()   # SDK smart logic
    return breakout, intraday
