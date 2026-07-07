from moving_average import ema, alma
from mad import mad
from system import system
from signal_engine import (
    generate_signal,
    generate_bb_signal,
    generate_combined_signal,
)

from config import *


def calculate_indicators(df):

    # ========= EMA =========

    df["EMA25"] = ema(df["close"], EMA_LENGTH)

    # ========= ALMA =========

    df["ALMA10"] = alma(df["close"], ALMA_LENGTH)

    # ========= MAD =========

    df["MAD25"] = mad(df["close"], df["EMA25"], EMA_LENGTH)

    df["MAD2"] = mad(df["close"], df["ALMA10"], ALMA_LENGTH)

    # ========= MAD Weighted =========

    df["MAD_W_NUM"] = alma(
        df["close"] * df["MAD2"],
        ALMA_LENGTH,
    )

    df["MAD_W_DEN"] = alma(
        df["MAD2"],
        ALMA_LENGTH,
    )

    df["MAD_W_SRC"] = (
        df["MAD_W_NUM"]
        /
        df["MAD_W_DEN"]
    )

    # ========= FOR LOOP =========

    df["MAD_FL"] = system(
        df["MAD_W_SRC"],
        FROM_BAR,
        TO_BAR,
    )

    # ========= SCORE =========

    df["SCORE"] = generate_signal(
        df["MAD_FL"],
        LONG_THRESHOLD,
        SHORT_THRESHOLD,
    )

    # ========= BB =========

    df["Upper"] = (
        df["EMA25"]
        +
        df["MAD25"] * UPPER_MULTIPLIER
    )

    df["Lower"] = (
        df["EMA25"]
        -
        df["MAD25"] * LOWER_MULTIPLIER
    )

    # ========= BB SCORE =========

    df["BB_SCORE"] = generate_bb_signal(
        df["close"],
        df["Upper"],
        df["Lower"],
    )

    # ========= COMBINED =========

    df["COMBINED"] = (
        df["BB_SCORE"]
        +
        df["SCORE"]
    ) / 2

    df["FINAL_SCORE"] = generate_combined_signal(
        df["COMBINED"],
        COMBINED_LONG,
        COMBINED_SHORT,
    )

    return df