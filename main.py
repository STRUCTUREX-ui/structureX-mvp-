import requests

API_KEY = "08a5cc9c85f8439680bb3e8e4eb77a24"

def fetch_xauusd_daily():
    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": "XAU/USD",
        "interval": "1day",
        "outputsize": 50,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data


def extract_candles(data):
    candles = data["values"]
    candles = candles[::-1]  # Oldest first

    cleaned_candles = []

    for candle in candles:
        cleaned_candles.append({
            "datetime": candle["datetime"],
            "open": float(candle["open"]),
            "high": float(candle["high"]),
            "low": float(candle["low"]),
            "close": float(candle["close"])
        })

    return cleaned_candles


def detect_swings(candles):
    swings = []

    for i in range(1, len(candles) - 1):

        prev_candle = candles[i - 1]
        current_candle = candles[i]
        next_candle = candles[i + 1]

        # Swing High
        if current_candle["high"] > prev_candle["high"] and current_candle["high"] > next_candle["high"]:
            swings.append({
                "type": "swing_high",
                "price": current_candle["high"],
                "datetime": current_candle["datetime"]
            })

        # Swing Low
        if current_candle["low"] < prev_candle["low"] and current_candle["low"] < next_candle["low"]:
            swings.append({
                "type": "swing_low",
                "price": current_candle["low"],
                "datetime": current_candle["datetime"]
            })

    return swings


data = fetch_xauusd_daily()
candles = extract_candles(data)
swings = detect_swings(candles)

# Print last 10 swings
for swing in swings[-10:]:
    print(swing)
