# services/signal_store.py

signal_times = {}

def get_signal_time(symbol):
    return signal_times.get(symbol)

def set_signal_time(symbol, time):
    if symbol not in signal_times:
        signal_times[symbol] = time
