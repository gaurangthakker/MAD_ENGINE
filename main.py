import json
import requests
import pandas as pd
from datetime import datetime
from system import system
from config import *
from signal_engine import generate_signal,generate_bb_signal,generate_combined_signal
from trade_logger import create_trade_log
from analytics import generate_summary
from report import create_html_report
from indicator_engine import calculate_indicators

from moving_average import ema, alma
from mad import mad


# ==========================
# CONFIG
# ==========================

TOKEN_FILE = r"H:\My Drive\MAD INDICATOR\MAD_ENGINE\upstox_login\token.json"

SYMBOL = "ABB"
INSTRUMENT_KEY = "NSE_EQ|INE117A01022"


# ==========================
# ACCESS TOKEN
# ==========================

def get_access_token():
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)["access_token"]


# ==========================
# HISTORICAL DATA
# ==========================

def get_historical_data(token, instrument_key, day):

    date_str = day.strftime("%Y-%m-%d")

    url = (
        f"https://api.upstox.com/v3/historical-candle/"
        f"{instrument_key}/minutes/1/{date_str}/{date_str}"
    )

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(r.text)
        return None

    data = r.json()

    candles = data["data"]["candles"]

    df = pd.DataFrame(
        candles,
        columns=[
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "oi"
        ]
    )

    # Reverse because Upstox gives latest candle first
    df = df.iloc[::-1].reset_index(drop=True)

    # Datetime conversion
    df["datetime"] = pd.to_datetime(df["datetime"])

    return df


# ==========================
# MAIN
# ==========================

def main():

    token = get_access_token()

    day = datetime(2026, 7, 3)

    df = get_historical_data(
        token,
        INSTRUMENT_KEY,
        day
    )

    if df is None :
        return
        
    # ========INDICATORS========
    df = calculate_indicators(df)
  
    # ========= PRINT =========

    def main():

        print(
        df[
            (df["BB_SCORE"] != df["BB_SCORE"].shift(1)) |
            (df["SCORE"] != df["SCORE"].shift(1))
        ][
            [
                "datetime",
                "close",
                "BB_SCORE",
                "SCORE",
                "COMBINED",
                "FINAL_SCORE"
            ]
        ]
    )

    buy_signals = (
    (df["FINAL_SCORE"] == 1) &
    (df["FINAL_SCORE"].shift(1) != 1)).sum()

    sell_signals = (
    (df["FINAL_SCORE"] == -1) &
    (df["FINAL_SCORE"].shift(1) != -1)).sum()

    print("Actual BUY Signals :", buy_signals)
    print("Actual SELL Signals:", sell_signals)

    buy_rows = df[
    (df["FINAL_SCORE"] == 1) &
    (df["FINAL_SCORE"].shift(1) != 1)][["datetime", "close"]]

    sell_rows = df[
    (df["FINAL_SCORE"] == -1) &
    (df["FINAL_SCORE"].shift(1) != -1)][["datetime", "close"]]

    print("\nBUY Entries")
    print(buy_rows)

    print("\nSELL Entries")
    print(sell_rows)

    signals = df[
    ((df["FINAL_SCORE"] == 1) & (df["FINAL_SCORE"].shift(1) != 1)) |
    ((df["FINAL_SCORE"] == -1) & (df["FINAL_SCORE"].shift(1) != -1))][["datetime", "close", "FINAL_SCORE"]].copy()

    signals["SIGNAL"] = signals["FINAL_SCORE"].map({1: "BUY",-1: "SELL"})

    signals.to_csv("reports/signals.csv", index=False)

    print("\nSignals exported to signals.csv")
    print(signals)

    trade_log = create_trade_log(signals)

    print("\nTrade Log")
    print(trade_log)

    trade_log.to_csv("reports/trade_log.csv", index=False)

    print("\nTrade Log exported to trade_log.csv")

    summary = generate_summary(trade_log)

    print("\n========== BACKTEST SUMMARY ==========")

    for key, value in summary.items():
        print(f"{key:15}: {value}")

    create_html_report(summary, df)


if __name__ == "__main__":
    main()