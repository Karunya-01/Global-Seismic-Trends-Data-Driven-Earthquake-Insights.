import pandas as pd
import numpy as np
import re

# =========================================
# COUNTRY EXTRACTION
# =========================================
def extract_country(place):
    if pd.isna(place):
        return "Unknown"

    match = re.search(r",\s*([^,]+)$", place)
    if match:
        return match.group(1).strip()

    return "Unknown"


# =========================================
# DEPTH CATEGORY
# =========================================
def depth_category(depth):
    if pd.isna(depth):
        return "Unknown"
    if depth < 70:
        return "Shallow"
    elif depth < 300:
        return "Intermediate"
    else:
        return "Deep"


# =========================================
# MAG CATEGORY
# =========================================
def magnitude_category(mag):
    if pd.isna(mag):
        return "Unknown"
    if mag < 4:
        return "Minor"
    elif mag < 6:
        return "Moderate"
    elif mag < 7:
        return "Strong"
    else:
        return "Major"


# =========================================
# MAIN CLEANING FUNCTION
# =========================================
def clean_data():

    df = pd.read_csv("data/earthquake_raw.csv")

    # ---------- TIME ----------
    df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")
    df["updated"] = pd.to_datetime(df["updated"], unit="ms", errors="coerce")

    # ---------- NUMERIC ----------
    numeric_cols = [
        "mag", "depth_km", "nst", "dmin", "rms", "gap",
        "magError", "depthError", "magNst", "sig"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df[numeric_cols] = df[numeric_cols].fillna(0)

    # ---------- TEXT ----------
    text_cols = [
        "magType", "status", "net", "locationSource",
        "magSource", "types", "ids", "sources", "type"
    ]

    for col in text_cols:
        df[col] = df[col].astype(str).str.lower().str.strip()

    df["alert"] = df["alert"].astype(str).str.lower()

    # ---------- COUNTRY ----------
    df["country"] = df["place"].apply(extract_country)

    # ---------- DERIVED TIME ----------
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"] = df["time"].dt.day
    df["day_of_week"] = df["time"].dt.day_name()
    df["hour"] = df["time"].dt.hour

    # ---------- DERIVED SEISMIC ----------
    df["depth_category"] = df["depth_km"].apply(depth_category)
    df["mag_category"] = df["mag"].apply(magnitude_category)

    df["is_shallow"] = np.where(df["depth_km"] < 50, 1, 0)
    df["is_strong"] = np.where(df["mag"] >= 7.5, 1, 0)

    # ---------- FINAL ----------
    df = df.drop_duplicates(subset="id")

    df.to_csv("data/earthquake_cleaned.csv", index=False)

    print("✅ Cleaned data saved")


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    clean_data()
