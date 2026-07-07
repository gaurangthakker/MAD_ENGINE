import pandas as pd

def generate_signal(mad_fl, long_level, short_level):

    state = 0
    result = []

    for i in range(len(mad_fl)):

        if i == 0:
            result.append(state)
            continue

        prev = mad_fl.iloc[i-1]
        curr = mad_fl.iloc[i]

        # Cross Above Long Threshold
        if prev <= long_level and curr > long_level:
            state = 1

        # Cross Below Short Threshold
        elif prev >= short_level and curr < short_level:
            state = -1

        result.append(state)

    return pd.Series(result, index=mad_fl.index)

import pandas as pd

def generate_bb_signal(close, upper, lower):

    state = 0
    result = []

    for i in range(len(close)):

        if i == 0:
            result.append(0)
            continue

        # Cross Above Upper Band
        if close.iloc[i-1] <= upper.iloc[i-1] and close.iloc[i] > upper.iloc[i]:
            state = 1

        # Cross Below Lower Band
        elif close.iloc[i-1] >= lower.iloc[i-1] and close.iloc[i] < lower.iloc[i]:
            state = -1

        result.append(state)

    return pd.Series(result, index=close.index)

def generate_combined_signal(combined, long_level=0, short_level=0):

    state = 0
    result = []

    for i in range(len(combined)):

        if i == 0:
            result.append(0)
            continue

        prev = combined.iloc[i-1]
        curr = combined.iloc[i]

        # Ignore NaN values
        if pd.isna(prev) or pd.isna(curr):
            result.append(state)
            continue

        if prev <= long_level and curr > long_level:
            state = 1

        elif prev >= short_level and curr < short_level:
            state = -1

        result.append(state)

    return pd.Series(result, index=combined.index)
