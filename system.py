import pandas as pd
import numpy as np


def system(series, start, end):

    result = []

    for current in range(len(series)):

        if current < end:
            result.append(np.nan)
            continue

        total = 0

        current_value = series.iloc[current]

        for i in range(start, end + 1):

            past_value = series.iloc[current - i]

            if current_value > past_value:
                total += 1
            else:
                total -= 1

        result.append(total)

    return pd.Series(result, index=series.index)