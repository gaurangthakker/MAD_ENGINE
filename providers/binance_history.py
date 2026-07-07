import requests
import pandas as pd


class BinanceHistory:

    def __init__(self, symbol="BTCUSDT", interval="1m", limit=200):

        self.symbol = symbol.upper()
        self.interval = interval
        self.limit = limit

    def download(self):

        url = (
            "https://api.binance.com/api/v3/klines"
            f"?symbol={self.symbol}"
            f"&interval={self.interval}"
            f"&limit={self.limit}"
        )

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(
            data,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "number_of_trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore",
            ],
        )

        df = df[
            [
                "open_time",
                "open",
                "high",
                "low",
                "close",
            ]
        ]

        df.rename(
            columns={
                "open_time": "datetime"
            },
            inplace=True,
        )

        df["datetime"] = pd.to_datetime(
            df["datetime"],
            unit="ms",
        )

        for col in [
            "open",
            "high",
            "low",
            "close",
        ]:

            df[col] = df[col].astype(float)

        return df