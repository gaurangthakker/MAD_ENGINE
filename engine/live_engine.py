import pandas as pd
import requests

from status_writer import write_signal
from indicator_engine import calculate_indicators

BOT_TOKEN = "8716806437:AAFWc5FOSOgwT6sdIEFZonnK5zypoLU4uMg"
CHAT_ID = "6442905123"


class LiveEngine:

    def __init__(self, symbol, df=None):

        self.symbol = symbol

        if df is None:
            self.df = pd.DataFrame(
                columns=[
                    "datetime",
                    "open",
                    "high",
                    "low",
                    "close",
                ]
            )
        else:
            self.df = df.copy().reset_index(drop=True)

        self.last_signal = 0

        print(f"{self.symbol} : {len(self.df)} History Candles Loaded")

    def send_telegram(self, message):
        try:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": CHAT_ID,
                    "text": message
                },
                timeout=10
            )
        except Exception as e:
            print("Telegram Error:", e)

    def process_candle(self, candle):

        new_row = {
            "datetime": candle["time"],
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
        }

        self.df.loc[len(self.df)] = new_row

        if len(self.df) > 200:
            self.df = self.df.iloc[-200:].reset_index(drop=True)

        self.df = calculate_indicators(self.df)

        last = self.df.iloc[-1]

        if pd.isna(last["FINAL_SCORE"]):
            return

        write_signal(self.symbol, last)

        signal = int(last["FINAL_SCORE"])

        if signal != self.last_signal:

            print("\n==================================")

            if signal == 1:
                print(f"🚀 BUY SIGNAL ({self.symbol})")
            elif signal == -1:
                print(f"🔻 SELL SIGNAL ({self.symbol})")

            print("==================================")
            print(f"Time        : {last['datetime']}")
            print(f"Price       : {last['close']:.2f}")
            print(f"EMA25       : {last['EMA25']:.2f}")
            print(f"ALMA10      : {last['ALMA10']:.2f}")
            print(f"MAD_FL      : {int(last['MAD_FL'])}")
            print(f"BB_SCORE    : {int(last['BB_SCORE'])}")
            print(f"SCORE       : {int(last['SCORE'])}")
            print(f"FINAL_SCORE : {int(last['FINAL_SCORE'])}")
            print("==================================")

            emoji = "🟢" if signal == 1 else "🔴"
            text = "BUY" if signal == 1 else "SELL"

            msg = (
                f"🚀 MAD ENGINE ALERT\n\n"
                f"{emoji} {text} SIGNAL\n\n"
                f"Symbol : {self.symbol}\n"
                f"Price  : {last['close']:.2f}\n\n"
                f"EMA25  : {last['EMA25']:.2f}\n"
                f"ALMA10 : {last['ALMA10']:.2f}\n"
                f"MAD_FL : {int(last['MAD_FL'])}\n"
                f"BB_SCORE : {int(last['BB_SCORE'])}\n"
                f"SCORE : {int(last['SCORE'])}\n"
                f"FINAL_SCORE : {int(last['FINAL_SCORE'])}\n\n"
                f"Time : {last['datetime']}"
            )

            self.send_telegram(msg)

            self.last_signal = signal