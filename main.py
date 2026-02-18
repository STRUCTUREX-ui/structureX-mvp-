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

    # Reverse list so oldest candle comes first
    candles = candles[::-1]

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


data = fetch_xauusd_daily()
candles = extract_candles(data)

# Print last 10 candles
for candle in candles[-10:]:
    print(candle)
