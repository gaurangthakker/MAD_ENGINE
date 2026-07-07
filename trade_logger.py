import pandas as pd


def create_trade_log(signals: pd.DataFrame) -> pd.DataFrame:
    """
    Create completed trades from BUY/SELL signals.
    """

    trades = []

    trade_id = 1

    for i in range(len(signals) - 1):

        entry = signals.iloc[i]
        exit = signals.iloc[i + 1]

        side = "LONG" if entry["SIGNAL"] == "BUY" else "SHORT"

        entry_price = entry["close"]
        exit_price = exit["close"]

        if side == "LONG":
            points = exit_price - entry_price
        else:
            points = entry_price - exit_price

        trades.append(
            {
                "Trade ID": trade_id,
                "Side": side,
                "Entry Time": entry["datetime"],
                "Entry Price": entry_price,
                "Exit Time": exit["datetime"],
                "Exit Price": exit_price,
                "Points": round(points, 2),
            }
        )

        trade_id += 1

    return pd.DataFrame(trades)