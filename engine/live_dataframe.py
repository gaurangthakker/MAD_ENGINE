import pandas as pd


class LiveDataFrame:

    def __init__(self, max_rows=500):

        self.max_rows = max_rows

        self.df = pd.DataFrame(
            columns=[
                "datetime",
                "open",
                "high",
                "low",
                "close"
            ]
        )

    def add_candle(self, candle):

        self.df.loc[len(self.df)] = [
            candle["time"],
            candle["open"],
            candle["high"],
            candle["low"],
            candle["close"],
        ]

        if len(self.df) > self.max_rows:

            self.df = (
                self.df
                .iloc[-self.max_rows:]
                .reset_index(drop=True)
            )

        return self.df