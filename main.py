# main.py

import time
from kiwoom_api import KiwoomAPI
from indicators import calculate_sma, calculate_rsi_wilder
from strategy import select_candidates
from utils import save_to_csv


def main():
    """
    1) KOSPI 시장 종목 코드 수집
    2) 종목별 과거 51거래일 이상 종가 데이터 요청
    3) MA20, MA50, RSI 계산
    4) 매수 후보 분류 (A/B/C 그룹)
    5) 후보 CSV 저장
    """
    api = KiwoomAPI()

    try:
        print("[Info] 로그인 시도 중...")
        api.login()
        print("[Info] 로그인 성공")
    except Exception as e:
        print(f"[Error] 로그인 실패: {e}")
        return

    print("[Info] KOSPI 종목 코드 수집 중...")
    codes = api.get_kospi_codes()
    print(f"[Info] 수집된 KOSPI 종목 수: {len(codes)}")

    candidates = []

    for idx, code in enumerate(codes, start=1):
        # 진행 상황 출력
        print(f"[{idx}/{len(codes)}] 코드: {code} 데이터 수집 중...")

        # 1) 과거 51일 이상 종가 데이터 요청
        df_price = api.get_price_data(code, count=51)
        if df_price is None or len(df_price) < 51:
            print(f"[Warning] {code} 데이터 부족 또는 오류")
            continue

        # 2) 이동평균(MA20, MA50) 계산
        df_price["MA20"] = calculate_sma(
            df_price["Close"], 20
        )  # 책 13장 SMA 참조 :contentReference[oaicite:37]{index=37}
        df_price["MA50"] = calculate_sma(df_price["Close"], 50)

        # 3) RSI 계산 (Wilder SMMA)
        df_price["RSI"] = calculate_rsi_wilder(
            df_price["Close"], 14
        )  # 책 13장 RSI 참조 :contentReference[oaicite:38]{index=38}

        # 4) 종목명 수집
        name = api.get_stock_name(code)
        if name is None:
            name = "Unknown"

        # 5) 매수 후보 분류
        candidate = select_candidates(code, name, df_price)
        if candidate:
            candidates.append(candidate)
            print(f"  → 후보 선정: {code} ({name}), 그룹={candidate['group']}")

        # 6) 호출 제한 대응: 종목별 최소 0.2초 대기 권장, 에러 시 추가 대기
        time.sleep(0.2)

    # 7) 결과 저장
    print("[Info] 후보 리스트 저장 중...")
    save_to_csv(candidates, base_filename="candidates")


if __name__ == "__main__":
    main()
