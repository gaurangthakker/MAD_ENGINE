from datetime import datetime


class CandleBuilder:

    def __init__(self):

        self.current_minute = None
        self.candle = None

    def update(self, price):

        now = datetime.now().replace(second=0, microsecond=0)

        # New 1-minute candle
        if self.current_minute != now:

            finished = self.candle

            self.current_minute = now

            self.candle = {
                "time": now,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
            }

            return finished

        # Update current candle
        self.candle["high"] = max(self.candle["high"], price)
        self.candle["low"] = min(self.candle["low"], price)
        self.candle["close"] = price

        return None