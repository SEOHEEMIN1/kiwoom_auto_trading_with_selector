import numpy as np
import pandas as pd

from indicators import calculate_sma, calculate_rsi_wilder


def test_calculate_sma_simple():
    series = pd.Series([1, 2, 3, 4, 5])
    result = calculate_sma(series, 3)
    expected = pd.Series([np.nan, np.nan, 2.0, 3.0, 4.0])
    assert result.equals(expected)


def test_calculate_rsi_all_gain():
    series = pd.Series(range(1, 21))
    rsi = calculate_rsi_wilder(series, 14)
    assert rsi.iloc[:14].isna().all()
    assert (rsi.iloc[14:] == 100).all()


def test_calculate_rsi_all_loss():
    series = pd.Series(range(20, 0, -1))
    rsi = calculate_rsi_wilder(series, 14)
    assert rsi.iloc[:14].isna().all()
    assert (rsi.iloc[14:] == 0).all()
