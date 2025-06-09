# indicators.py

import pandas as pd
import numpy as np


def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    """
    단순 이동 평균(SMA) 계산
    - pandas.Series.rolling(window=period).mean()
    """
    return series.rolling(window=period, min_periods=period).mean()


def calculate_rsi_wilder(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Wilder의 SMMA 방식 RSI 계산 (기본 period=14)
    1) price 변화량(delta) 계산
    2) gain, loss로 분리
    3) 초기 avg_gain, avg_loss는 첫 period의 단순평균(SMA)
    4) 이후 SMMA 재귀식:
       avg_gain[i] = (prev_avg_gain * (period - 1) + gain[i]) / period
       avg_loss[i] = (prev_avg_loss * (period - 1) + loss[i]) / period
    5) RS = avg_gain / avg_loss, RSI = 100 - (100 / (1 + RS))
    - period 구간 이전에는 NaN 발생
    - Wikipedia “Relative Strength Index” 정의 참고 :contentReference[oaicite:26]{index=26}
    - GitHub 예시: wilders_rsi_pandas.py :contentReference[oaicite:27]{index=27}
    """
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rsi = pd.Series(np.nan, index=series.index)

    if len(series) <= period:
        return rsi

    if avg_loss.iloc[period] == 0:
        rsi.iloc[period] = 100
    else:
        rs_first = avg_gain.iloc[period] / avg_loss.iloc[period]
        rsi.iloc[period] = 100 - (100 / (1 + rs_first))

    for i in range(period + 1, len(series)):
        prev_avg_gain = avg_gain.iloc[i - 1]
        prev_avg_loss = avg_loss.iloc[i - 1]
        current_gain = gain.iat[i]
        current_loss = loss.iat[i]

        avg_gain.iloc[i] = (prev_avg_gain * (period - 1) + current_gain) / period
        avg_loss.iloc[i] = (prev_avg_loss * (period - 1) + current_loss) / period

        if avg_loss.iloc[i] == 0:
            rsi.iloc[i] = 100
        else:
            rs = avg_gain.iloc[i] / avg_loss.iloc[i]
            rsi.iloc[i] = 100 - (100 / (1 + rs))

    return rsi
