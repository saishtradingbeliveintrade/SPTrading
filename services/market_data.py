import requests
from config import UPSTOX_ACCESS_TOKEN
from instrument_map import INSTRUMENT_MAP   # <- हा file वेगळा ठेव

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}


def get_ltp(symbol: str):
    key = INSTRUMENT_MAP.get(symbol.upper())

    if not key:
        return {"error": "Invalid symbol"}

    url = f"https://api.upstox.com/v3/market-quote/ltp?instrument_key={key}"
    res = requests.get(url, headers=HEADERS)
    return res.json()
