import requests

BOD_URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json"

def load_instruments():
    data = requests.get(BOD_URL).json()

    instrument_map = {}

    for item in data:
        if item.get("segment") == "NSE_EQ" and item.get("instrument_type") == "EQ":
            symbol = item.get("trading_symbol")
            instrument_key = item.get("instrument_key")
            if symbol and instrument_key:
                instrument_map[symbol] = instrument_key

    print(f"Loaded {len(instrument_map)} NSE_EQ instruments")
    return instrument_map
