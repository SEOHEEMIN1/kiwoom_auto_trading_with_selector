import pandas as pd

from strategy import select_candidates


def make_df(group: str) -> pd.DataFrame:
    """Return DataFrame of length 51 to trigger a specific group."""

    close = [100] * 51
    if group == "A":
        ma20 = [1] * 50 + [2]
        ma50 = [1] * 51
        rsi = [50] * 50 + [40]  # not oversold
    elif group == "B":
        ma20 = [1] * 51
        ma50 = [1] * 51
        rsi = [50] * 50 + [20]  # oversold only
    elif group == "C":
        ma20 = [1] * 50 + [2]
        ma50 = [1] * 51
        rsi = [50] * 50 + [20]
    else:
        ma20 = [1] * 51
        ma50 = [1] * 51
        rsi = [50] * 51

    return pd.DataFrame(
        {
            "Close": close,
            "MA20": ma20,
            "MA50": ma50,
            "RSI": rsi,
        }
    )


def test_select_candidates_group_a():
    df = make_df("A")
    result = select_candidates("000111", "TESTA", df)
    assert result is not None
    assert result["group"] == "A"


def test_select_candidates_group_b():
    df = make_df("B")
    result = select_candidates("000222", "TESTB", df)
    assert result is not None
    assert result["group"] == "B"


def test_select_candidates_group_c():
    df = make_df("C")
    result = select_candidates("000000", "TEST", df)
    assert result is not None
    assert result["group"] == "C"


def test_select_candidates_no_signal():
    df = make_df("N")
    assert select_candidates("000333", "TEST", df) is None


def test_select_candidates_with_nan():
    df = make_df("C")
    df.loc[50, "MA20"] = float("nan")
    assert select_candidates("000444", "TEST", df) is None


def test_select_candidates_insufficient():
    df = make_df("A").iloc[:50]
    assert select_candidates("000000", "TEST", df) is None
