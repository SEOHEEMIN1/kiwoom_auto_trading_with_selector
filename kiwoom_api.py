# kiwoom_api.py

import time
from datetime import datetime
from pykiwoom.kiwoom import Kiwoom
import pandas as pd


class KiwoomAPI:
    def __init__(self):
        """
        PyKiwoom Kiwoom 객체 생성
        """
        self.kiwoom = Kiwoom()

    def login(self):
        """
        Kiwoom OpenAPI+ 로그인
        - CommConnect(block=True) 호출 후 연결 상태 확인
        """
        self.kiwoom.CommConnect(block=True)
        # 연결 상태 확인 (연결 실패 시 예외 발생)
        if self.kiwoom.GetConnectState() == 0:
            raise ConnectionError(
                "Kiwoom API 연결 실패"
            )  # 책 3장 06) 연결 상태 확인 :contentReference[oaicite:14]{index=14}

    def get_kospi_codes(self):
        """
        KOSPI 시장(코드 '0')의 전체 종목 코드 리스트 반환
        """
        codes = self.kiwoom.GetCodeListByMarket(
            "0"
        )  # 시장 코드 '0' = KOSPI :contentReference[oaicite:15]{index=15}
        return codes.split(";") if isinstance(codes, str) else []

    def get_price_data(self, code, count=50):
        """
        특정 종목 코드에 대해 과거 'count' 거래일치 일별 종가 데이터를 수집.
        1) opt10081 TR(주식일봉차트조회) 호출
        2) 페이징(next 인자 활용) 처리
        3) 종가(컬럼명 '현재가' 혹은 '종가')만 float으로 변환
        4) 데이터프레임을 날짜 오름차순으로 정렬 후 반환
        - 호출 제한을 준수하기 위해 sleep 삽입
        - 예외 발생 시 None 반환
        """
        all_data = []  # 페이지별 데이터를 하나로 합치기 위한 리스트
        next_flag = 0  # next 인자: 0은 첫 페이지, 이후 2로 시작
        today_str = datetime.today().strftime(
            "%Y%m%d"
        )  # 동적 기준일자 설정 :contentReference[oaicite:16]{index=16}

        while True:
            try:
                # opt10081: 주식일봉차트조회 (책 7장 01) 싱글데이터 TR 사용하기 및 7장 02) 멀티데이터 TR 사용하기 :contentReference[oaicite:17]{index=17})
                result = self.kiwoom.block_request(
                    "opt10081",
                    종목코드=code,
                    기준일자=today_str,
                    수정주가구분=1,
                    output="주식일봉차트조회",
                    next=next_flag,
                )
                # TR 호출 후 호출 제한 회피용 딜레이: 최소 0.2초 이상 권장 :contentReference[oaicite:18]{index=18}
                time.sleep(0.2)

                # 결과가 DataFrame 형태이면 바로 처리, 아니면 DataFrame으로 변환
                df_part = pd.DataFrame(result)
                if df_part.empty:
                    break

                # 컬럼 중 '현재가' 혹은 '종가' 컬럼이 존재하는지 확인
                # pykiwoom에서 반환 시 key가 '현재가'인 경우가 많으므로, '현재가'를 사용
                if "현재가" not in df_part.columns and "종가" not in df_part.columns:
                    # 컬럼명이 다르면 예외 발생
                    raise KeyError(
                        f"{code} TR 반환 컬럼에 '현재가' 또는 '종가'가 없습니다."
                    )

                # 종가 컬럼만 float으로 변환
                price_col = "현재가" if "현재가" in df_part.columns else "종가"
                df_part = df_part[[price_col]].astype(float)

                # 인덱스가 뒤집혀 있으므로 날짜 내림차순 → 오름차순으로 재정렬
                df_part = df_part.iloc[::-1].reset_index(drop=True)
                all_data.append(df_part)

                # 'Next' 값 확인: '2'(문자열)로 내려갈 수 있으면 계속, 아니면 종료
                if result.get("Next") == "2":
                    next_flag = 2
                else:
                    break

            except Exception as e:
                print(f"[Error] {code} 데이터 수집 중 오류: {e}")
                return None  # 예외 발생 시 None 반환

        if not all_data:
            return None

        # 모든 페이징 결과 합치기
        df_full = pd.concat(all_data, ignore_index=True)
        # 50거래일 이상인지 검사
        if len(df_full) < count:
            return None

        # 최근 count일치 데이터만 남기기
        df_full = df_full.iloc[-count:].reset_index(drop=True)
        df_full.columns = ["Close"]  # 컬럼명 일관성 유지: 'Close'
        return df_full

    def get_stock_name(self, code):
        """
        특정 코드의 종목명을 반환
        """
        try:
            name = self.kiwoom.GetMasterCodeName(
                code
            )  # 책 3장 05) 종목명 얻기 :contentReference[oaicite:19]{index=19}
            return name.strip()
        except Exception:
            return None
