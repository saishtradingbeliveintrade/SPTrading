import random

def get_live_data():
    return [
        {"name": "RELIANCE", "price": round(random.uniform(2400, 2600), 2)},
        {"name": "TCS", "price": round(random.uniform(3500, 3700), 2)},
        {"name": "INFY", "price": round(random.uniform(1400, 1500), 2)},
    ]
