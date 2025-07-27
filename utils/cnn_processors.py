from datetime import datetime, timedelta
import pandas as pd

def extract_stock_info(data):

    # Get specific fields from the first record
    first = data[0]
    latest = first.get("latest_ticker_data", {})

    # Get all P/E ratios from the rest of the records
    pe_ratios = [
        stock.get("pe_ratio") for stock in data[1:] 
        if stock.get("pe_ratio") is not None
    ]

    # Find largest and smallest P/E ratios
    largest_pe = max(pe_ratios) if pe_ratios else None
    smallest_pe = min(pe_ratios) if pe_ratios else None

    return {
        "name": first.get("name"),
        "market_cap": first.get("market_cap"),
        "market_volume": latest.get("market_volume"),
        "pe_ratio": first.get("pe_ratio"),
        "num_of_employees": first.get("num_of_employees"),
        "current_price": latest.get("current_price"),
        "close_price": latest.get("close_price"),
        "low_52_week": latest.get("low_52_week"),
        "high_52_week": latest.get("high_52_week"),
        "largest_competitor_pe": largest_pe,
        "smallest_competitor_pe": smallest_pe
    }

def calculate_price_change_summary(data):
    data.sort(key=lambda x: x["event_date"])
    price_by_date = {
        datetime.strptime(entry["event_date"], "%Y-%m-%d").date(): entry["current_price"]
        for entry in data if entry.get("current_price") is not None
    }

    all_dates = sorted(price_by_date.keys())
    latest_date = all_dates[-1]
    latest_price = price_by_date[latest_date]

    def calc_change_percent(old, new):
        return ((new - old) / old) * 100 if old else None

    def get_nearest_date(target_date):
        candidates = [d for d in all_dates if d <= target_date]
        return candidates[-1] if candidates else None

    periods = {
        "1 Year": all_dates[0],
        "6 Months": latest_date - timedelta(days=182),
        "1 Month": latest_date - timedelta(days=30),
        "5 Days": latest_date - timedelta(days=5),
        "1 Day": latest_date - timedelta(days=1),
    }

    change_summary = {}
    for label, target in periods.items():
        if label == "1 Year":
            old_date = target
        else:
            old_date = get_nearest_date(target)

        if old_date:
            old_price = price_by_date[old_date]
            change = calc_change_percent(old_price, latest_price)
            change_summary[label] = {
                "from": old_date.isoformat(),
                "to": latest_date.isoformat(),
                "old_price": old_price,
                "latest_price": latest_price,
                "change_pct": round(change, 2)
            }

    return change_summary

def calculate_price_momentum(data):
    df = pd.DataFrame([
        {
            "date": datetime.strptime(entry["event_date"], "%Y-%m-%d"),
            "price": entry["current_price"]
        }
        for entry in data
        if entry.get("current_price") is not None and entry.get("event_date")
    ])

    df.sort_values("date", inplace=True)
    df["SMA_200"] = df["price"].rolling(window=200).mean()

    latest_row = df.dropna(subset=["SMA_200"]).iloc[-1]
    current_price = latest_row["price"]
    sma_200 = latest_row["SMA_200"]
    momentum_pct = ((current_price - sma_200) / sma_200) * 100

    return {
        "latest_date": latest_row["date"].date().isoformat(),
        "current_price": current_price,
        "sma_200": round(sma_200, 2),
        "momentum_pct": round(momentum_pct, 2)
    }
