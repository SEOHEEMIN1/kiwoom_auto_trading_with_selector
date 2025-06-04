````markdown
# AGENTS.md

## 프로젝트 개요
- **목적**: 코스피(KOSPI) 종목을 대상으로 매일 장 종료 후 자동으로 실행되어  
  1) 과거 50거래일치 종가 데이터를 수집  
  2) MA20, MA50, RSI(14) 지표를 계산  
  3) 골든크로스 및 RSI 과매도 조건을 기반으로 A·B·C 그룹으로 분류  
  4) 매수 후보 리스트(`candidates_YYYYMMDD.csv`)를 생성  
- **주요 파일**  
  - `main.py`: 워크플로우 시작점 (로그인 → 데이터 수집 → 지표 계산 → 후보 선정 → CSV 저장)  
  - `kiwoom_api.py`: PyKiwoom 로그인, KOSPI 종목 코드 수집, 페이징 처리된 일별 종가 수집  
  - `indicators.py`: SMA, Wilder SMMA 방식 RSI 계산  
  - `strategy.py`: A/B/C 그룹 분류 로직 (골든크로스·과매도 검사)  
  - `utils.py`: 날짜 기반 CSV 저장 유틸리티

## 개발 환경 설정
1. **Python 3.8 이상**  
2. **가상환경 생성 (권장)**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   # 또는 venv\Scripts\activate  # Windows
````

3. **의존성 설치**

   ```bash
   pip install --upgrade pip
   pip install pykiwoom pandas apscheduler python-dotenv
   ```
4. **환경 변수 (선택)**

   * Kiwoom 로그인 정보는 운영체제 환경 변수 또는 `.env` 파일로 관리
   * 예시 `.env` 파일:

     ```
     KIWOOM_USER=your_id
     KIWOOM_PW=your_password
     ```
   * 코드에서 `python-dotenv`를 사용해 로드하거나,

     ```python
     import os
     os.environ["KIWOOM_USER"]
     os.environ["KIWOOM_PW"]
     ```

## 파일 / 폴더 설명

* **`main.py`**

  * 전체 실행 흐름을 담당
  * Kiwoom 로그인 → 종목 코드 수집 → 일별 종가 조회 → 지표 계산 → 후보 선정 → CSV 저장
* **`kiwoom_api.py`**

  * `login()`: CommConnect로 로그인 및 연결 상태 확인
  * `get_kospi_codes()`: KOSPI 종목 코드 반환
  * `get_price_data(code, count)`: `opt10081` TR을 페이징 처리해 과거 `count`일치 종가 반환
  * `get_stock_name(code)`: 종목명 조회
* **`indicators.py`**

  * `calculate_sma(series, period)`: 단순 이동평균(SMA) 계산
  * `calculate_rsi_wilder(series, period)`: Wilder SMMA 방식 RSI 계산
* **`strategy.py`**

  * `select_candidates(code, name, df)`: MA 골든크로스 및 RSI 과매도 조건을 검사해 A/B/C 그룹 분류
* **`utils.py`**

  * `save_to_csv(data, base_filename)`: 날짜 기반 파일명(`base_filename_YYYYMMDD.csv`)으로 저장, UTF-8 BOM 포함

## 테스트 및 검증

1. **유닛 테스트 (pytest)**

   * 프로젝트 루트에 `tests/` 폴더에 `test_*.py` 파일을 둡니다.
   * 예: `tests/test_indicators.py`
   * 실행:

     ```bash
     pip install pytest
     pytest tests/
     ```
2. **Lint / Formatter**

   * `black .` 로 코드 포맷팅
   * `flake8 .` 또는 `pylint .` 로 린트 검사
3. **전체 흐름 확인**

   ```bash
   python main.py
   ```

   * “로그인 성공” 로그 확인
   * 최종적으로 `candidates_YYYYMMDD.csv` 파일 생성 여부 확인

## 코드 변경 시 유의 사항

* **종목명 포함 여부**:

  * `kiwoom_api.get_stock_name()` 사용해 반드시 종목명이 함께 조회되도록 합니다.
* **페이징 로직**:

  * `opt10081` TR 호출 시 `next` 플래그를 확인해 반복 호출하여 50거래일 이상 데이터 확보
* **결측치 검사**:

  * `strategy.select_candidates()`에서 MA20, MA50, RSI 모두 NaN인지 확인 후, NaN이 있으면 후보에서 제외
* **호출 제한 대응**:

  * TR 호출 후 `time.sleep(0.2)`을 최소한으로 포함해 분당 허용 호출량을 초과하지 않도록 합니다
* **파일명 및 인코딩**:

  * 결과 저장 시 `candidates_YYYYMMDD.csv` 형식 사용하는지 확인
  * `encoding='utf-8-sig'`로 저장하여 Excel 호환성 보장

## PR 및 커밋 컨벤션

* **브랜치 네이밍**

  ```
  feature/<간단한-설명>
  fix/<간단한-버그설명>
  docs/<문서-수정>
  ```
* **커밋 메시지 형식**

  ```
  feat: 새로운 기능 설명
  fix: 버그 수정 설명
  refactor: 코드 리팩터링 설명
  docs: 문서 수정 설명
  test: 테스트 추가/수정 설명
  chore: 기타 변경 (예: 의존성 업데이트)
  ```
* **PR 제목**

  ```
  [<모듈명>] <간단한 설명>
  ```

  * 예: `[strategy] 골든크로스 로직 수정`
* **PR 본문 포함 내용**

  1. 변경 내용 요약
  2. 테스트 방법 (예: `pytest tests/`, `python main.py`)
  3. 확인된 결과 스크린샷 또는 주요 로그
  4. 추가 참고 사항 (API 키 설정, 스케줄러 설정 등)

## Agent 작업 지침

* **우선 수정 대상**

  1. `kiwoom_api.py` → 로그인, TR 페이징, 예외 처리
  2. `indicators.py` → SMA/RSI 계산 로직
  3. `strategy.py` → A/B/C 그룹 분류 로직
  4. `main.py` → 워크플로우 제어 및 호출 제한 대응
  5. `utils.py` → CSV 저장 방식
* **작업 순서**

  1. AGENTS.md의 “개발 환경 설정”을 참고해 필요한 패키지 설치 및 가상환경 설정
  2. “테스트 및 검증”을 먼저 실행해 현재 상태를 확인
  3. 사용자가 요청한 변경사항을 한 파일씩 반영
  4. 변경 후 `black .`, `flake8 .`, `pytest tests/` 순으로 검사
  5. 로컬에서 CSV 저장 테스트 (`python main.py`)
  6. 변경사항 커밋 및 PR 생성 (커밋/PR 컨벤션 준수)
* **PR 메시지 작성 요령**

  * “What” (무엇을 바꿨는지)와 “Why” (왜 바꿨는지)를 명확히 기술
  * “How” (어떤 방식으로 구현했는지) 간략히 설명
  * 변경된 테스트 결과나 주요 로그를 첨부

## 추가 참고 링크

* **WikiDocs: 퀀트투자를 위한 키움증권 API (파이썬 버전)**
  [https://wikidocs.net/book/1173](https://wikidocs.net/book/1173)
* **Relative Strength Index (Wikipedia)**
  [https://en.wikipedia.org/wiki/Relative\_strength\_index](https://en.wikipedia.org/wiki/Relative_strength_index)

```
```
