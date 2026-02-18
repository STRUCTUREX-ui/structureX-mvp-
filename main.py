import requests

API_KEY = "08a5cc9c85f8439680bb3e8e4eb77a24"
SYMBOL = "XAU/USD"
INTERVAL = "1day"
OUTPUTSIZE = 200


# ===============================
# 1️⃣ Fetch Market Data
# ===============================

def fetch_market_data():
    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "apikey": API_KEY,
        "outputsize": OUTPUTSIZE
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "values" not in data:
        print("Error:", data)
        return None

    return data["values"]


# ===============================
# 2️⃣ Detect Swings (3-Candle Rule)
# ===============================

def detect_swings(data):
    swings = []

    for i in range(1, len(data) - 1):
        left = data[i - 1]
        current = data[i]
        right = data[i + 1]

        # Convert prices to float
        left_high = float(left["high"])
        current_high = float(current["high"])
        right_high = float(right["high"])

        left_low = float(left["low"])
        current_low = float(current["low"])
        right_low = float(right["low"])

        # Swing High
        if current_high > left_high and current_high > right_high:
            swings.append({
                "type": "swing_high",
                "price": current_high,
                "datetime": current["datetime"]
            })

        # Swing Low
        if current_low < left_low and current_low < right_low:
            swings.append({
                "type": "swing_low",
                "price": current_low,
                "datetime": current["datetime"]
            })

    return swings


# ===============================
# 3️⃣ Detect Trend (Last 3 Swings)
# ===============================

def detect_trend(swings):
    swing_highs = [s for s in swings if s["type"] == "swing_high"]
    swing_lows = [s for s in swings if s["type"] == "swing_low"]

    if len(swing_highs) < 3 or len(swing_lows) < 3:
        return "Not enough data"

    last_three_highs = swing_highs[-3:]
    last_three_lows = swing_lows[-3:]

    # Uptrend = Higher Highs + Higher Lows
    if (
        last_three_highs[0]["price"] < last_three_highs[1]["price"] < last_three_highs[2]["price"]
        and
        last_three_lows[0]["price"] < last_three_lows[1]["price"] < last_three_lows[2]["price"]
    ):
        return "Uptrend"

    # Downtrend = Lower Highs + Lower Lows
    if (
        last_three_highs[0]["price"] > last_three_highs[1]["price"] > last_three_highs[2]["price"]
        and
        last_three_lows[0]["price"] > last_three_lows[1]["price"] > last_three_lows[2]["price"]
    ):
        return "Downtrend"

    return "Sideways"


# ===============================
# 4️⃣ Main Execution
# ===============================

def main():
    print("Fetching market data...")
    data = fetch_market_data()

    if not data:
        return

    print("Detecting swings...")
    swings = detect_swings(data)

    print("Total Swings Found:", len(swings))

    trend = detect_trend(swings)

    print("Current Trend:", trend)


if name == "main":
    main()
