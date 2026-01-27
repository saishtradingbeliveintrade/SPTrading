import requests
from config import UPSTOX_ACCESS_TOKEN

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}

# RELIANCE instrument key example
INSTRUMENT_KEY = "NSE_EQ|INE002A01018"


def get_ltp():
    url = f"https://api.upstox.com/v3/market-quote/ltp?instrument_key={INSTRUMENT_KEY}"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def get_intraday_candle():
    url = f"https://api.upstox.com/v3/historical-candle/intraday/{INSTRUMENT_KEY}/minutes/5"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def get_historical_candle():
    url = f"https://api.upstox.com/v3/historical-candle/{INSTRUMENT_KEY}/days/1/2023-01-01/2023-12-31"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def get_live_data():
    ltp = get_ltp()
    return ltp
