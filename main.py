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

data = fetch_xauusd_daily()

print(data)
