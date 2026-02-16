import requests

API_KEY = "AHB89U36GOKB7YR4"

def fetch_xauusd_daily():
    url = "https://www.alphavantage.co/query"
    
    params = {
        "function": "FX_DAILY",
        "from_symbol": "XAU",
        "to_symbol": "USD",
        "apikey": API_KEY,
        "outputsize": "compact"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data


data = fetch_xauusd_daily()

print(data)
