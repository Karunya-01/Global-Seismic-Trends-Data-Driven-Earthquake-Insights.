import requests
import pandas as pd
from datetime import datetime, timedelta

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def fetch_month_data(start_date, end_date):
    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": 0
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print("Failed:", start_date)
        return []

    data = response.json()
    records = []

    for feature in data["features"]:
        prop = feature["properties"]
        geo = feature["geometry"]

        record = {
            "id": feature["id"],
            "time": prop.get("time"),
            "updated": prop.get("updated"),

            "latitude": geo["coordinates"][1] if geo else None,
            "longitude": geo["coordinates"][0] if geo else None,
            "depth_km": geo["coordinates"][2] if geo else None,

            "mag": prop.get("mag"),
            "magType": prop.get("magType"),
            "place": prop.get("place"),
            "status": prop.get("status"),
            "tsunami": prop.get("tsunami"),
            "sig": prop.get("sig"),
            "net": prop.get("net"),
            "nst": prop.get("nst"),
            "dmin": prop.get("dmin"),
            "rms": prop.get("rms"),
            "gap": prop.get("gap"),
            "magError": prop.get("magError"),
            "depthError": prop.get("depthError"),
            "magNst": prop.get("magNst"),
            "locationSource": prop.get("locationSource"),
            "magSource": prop.get("magSource"),
            "types": prop.get("types"),
            "ids": prop.get("ids"),
            "sources": prop.get("sources"),
            "type": prop.get("type"),
            "alert": prop.get("alert")
        }

        records.append(record)

    return records


def fetch_last_5_years():
    all_data = []
    today = datetime.today()

    for year in range(today.year - 5, today.year + 1):
        for month in range(1, 13):
            start = datetime(year, month, 1)

            if month == 12:
                end = datetime(year + 1, 1, 1)
            else:
                end = datetime(year, month + 1, 1)

            if start > today:
                break

            print(f"Fetching {start.date()}")

            records = fetch_month_data(
                start.strftime("%Y-%m-%d"),
                end.strftime("%Y-%m-%d")
            )

            all_data.extend(records)

    df = pd.DataFrame(all_data)
    return df


if __name__ == "__main__":
    df = fetch_last_5_years()
    df.to_csv("data/earthquake_raw.csv", index=False)
    print("Raw data saved")
