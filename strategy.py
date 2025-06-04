# strategy.py

import pandas as pd

def select_candidates(code: str, name: str, df: pd.DataFrame) -> dict:
    """
    df: DataFrame with columns ['Close', 'MA20', 'MA50', 'RSI'], index=날짜
    - 결측치 검사: 어제·오늘 MA20·MA50, 오늘 RSI 모두 NaN이 아니어야 함
    - 골든크로스: 어제 MA20 <= MA50 & 오늘 MA20 > MA50
    - 과매도: 오늘 RSI < 30
    - C그룹: 두 조건 모두 만족, A그룹: 골든크로스만, B그룹: 과매도만
    - 선택된 경우 { 'code','name','MA20','MA50','RSI','group' } 반환, 아니면 None
    """
    # 데이터 길이 최소 51일치(0~49: 지표 계산 구간, 50: 현재)
    if len(df) < 51:
        return None

    # 전일 인덱스 = -2, 당일 인덱스 = -1
    try:
        ma20_yesterday = df['MA20'].iloc[-2]
        ma50_yesterday = df['MA50'].iloc[-2]
        ma20_today = df['MA20'].iloc[-1]
        ma50_today = df['MA50'].iloc[-1]
        rsi_today = df['RSI'].iloc[-1]
    except Exception:
        return None

    # 결측치(NaN) 검사: 전일·당일 MA20·MA50, 당일 RSI 모두 유효해야 함 :contentReference[oaicite:29]{index=29}
    if pd.isna(ma20_yesterday) or pd.isna(ma50_yesterday) or pd.isna(ma20_today) or pd.isna(ma50_today) or pd.isna(rsi_today):
        return None

    # 골든크로스 여부
    golden_cross = (ma20_yesterday <= ma50_yesterday) and (ma20_today > ma50_today)
    # 과매도 여부
    oversold = (rsi_today < 30)  # RSI < 30: 과매도 신호 :contentReference[oaicite:30]{index=30}

    # 그룹 분류
    if golden_cross and oversold:
        group = 'C'
    elif golden_cross:
        group = 'A'
    elif oversold:
        group = 'B'
    else:
        return None

    return {
        'code': code,
        'name': name,
        'MA20': round(ma20_today, 2),
        'MA50': round(ma50_today, 2),
        'RSI': round(rsi_today, 2),
        'group': group
    }
