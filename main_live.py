from threading import Thread
import time

from providers.binance_history import BinanceHistory
from providers.binance import BinanceProvider


def start_symbol(symbol):

    print(f"\nLoading History : {symbol}")

    history = BinanceHistory(
        symbol=symbol,
        interval="1m",
        limit=200,
    )

    history_df = history.download()

    print(f"{symbol} History Loaded : {len(history_df)} Candles")

    provider = BinanceProvider(
        symbol=symbol.lower(),
        history_df=history_df,
    )

    provider.start()


btc_thread = Thread(
    target=start_symbol,
    args=("BTCUSDT",),
    daemon=True,
)

eth_thread = Thread(
    target=start_symbol,
    args=("ETHUSDT",),
    daemon=True,
)

btc_thread.start()
eth_thread.start()

while True:
    time.sleep(1)