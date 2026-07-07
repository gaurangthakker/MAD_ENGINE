import pandas as pd
import numpy as np


# ===================================
# EMA
# ===================================

def ema(series, length):
    return series.ewm(span=length, adjust=False).mean()


# ===================================
# ALMA
# TradingView Compatible
# ===================================

def alma(series, length, offset=0.85, sigma=6):

    m = offset * (length - 1)
    s = length / sigma

    weights = np.array([
        np.exp(-((i - m) ** 2) / (2 * s * s))
        for i in range(length)
    ])

    weights = weights / weights.sum()

    alma_values = []

    for i in range(len(series)):

        if i < length - 1:
            alma_values.append(np.nan)
            continue

        window = series.iloc[i - length + 1:i + 1].values

        value = np.sum(window * weights)

        alma_values.append(value)

    return pd.Series(alma_values, index=series.index)