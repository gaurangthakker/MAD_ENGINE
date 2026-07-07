import pandas as pd
import numpy as np


def mad(source, benchmark, length):

    result = []

    for current in range(len(source)):

        if current < length - 1:
            result.append(np.nan)
            continue

        bench = benchmark.iloc[current]

        total = 0.0

        for i in range(length):

            total += abs(
                source.iloc[current - i] - bench
            )

        result.append(total / length)

    return pd.Series(result, index=source.index)