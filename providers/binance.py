import json
import websocket

from status_writer import write_tick
from engine.candle_builder import CandleBuilder
from engine.live_engine import LiveEngine


class BinanceProvider:

    def __init__(self, symbol="btcusdt", history_df=None):

        self.symbol = symbol.lower()

        self.builder = CandleBuilder()

        self.engine = LiveEngine(
            self.symbol.upper(),
            history_df,
        )

    def on_message(self, ws, message):

        data = json.loads(message)

        price = float(data["c"])

        # Tick-by-Tick LTP Update
        write_tick(self.symbol.upper(), price)

        # Candle Builder
        candle = self.builder.update(price)

        if candle:

            print("\n==============================")
            print("1 Minute Candle Completed")
            print("==============================")
            print("Time :", candle["time"])
            print("Open :", candle["open"])
            print("High :", candle["high"])
            print("Low  :", candle["low"])
            print("Close:", candle["close"])

            # Process completed candle
            self.engine.process_candle(candle)

    def on_error(self, ws, error):

        print("\nERROR :", error)

    def on_close(self, ws, close_status_code, close_msg):

        print("\nDisconnected from Binance")

    def on_open(self, ws):

        print(f"\nConnected to Binance ({self.symbol.upper()})")

    def start(self):

        socket = (
            f"wss://stream.binance.com:9443/ws/"
            f"{self.symbol}@ticker"
        )

        ws = websocket.WebSocketApp(
            socket,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        ws.run_forever()