import pandas as pd


FLAT = 0
LONG = 1
SHORT = -1


def process_signals(signal: pd.Series):
    """
    Convert raw BUY/SELL signals into valid trading actions.

    Input
    -----
    signal
        1  = BUY signal
       -1  = SELL signal
        0  = No new signal

    Returns
    -------
    DataFrame
    Position
    Action
    """

    position = FLAT

    positions = []
    actions = []

    for s in signal:

        action = ""

        # -----------------------------
        # BUY
        # -----------------------------
        if s == 1:

            if position == FLAT:
                position = LONG
                action = "BUY"

            elif position == SHORT:
                position = LONG
                action = "REVERSE BUY"

            else:
                action = "IGNORE BUY"

        # -----------------------------
        # SELL
        # -----------------------------
        elif s == -1:

            if position == FLAT:
                position = SHORT
                action = "SELL"

            elif position == LONG:
                position = SHORT
                action = "REVERSE SELL"

            else:
                action = "IGNORE SELL"

        positions.append(position)
        actions.append(action)

    return pd.DataFrame(
        {
            "POSITION": positions,
            "ACTION": actions
        }
    )