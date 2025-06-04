# utils.py

import csv
from datetime import datetime

def save_to_csv(data: list, base_filename: str = "candidates"):
    """
    매수 후보 리스트를 CSV로 저장
    - data: [{ 'code','name','MA20','MA50','RSI','group' }, ...]
    - base_filename: 파일명 기본(예: 'candidates') → 'candidates_YYYYMMDD.csv'
    - UTF-8 BOM 포함 (encoding='utf-8-sig') :contentReference[oaicite:34]{index=34}
    """
    if not data:
        print("[Info] 저장할 데이터가 없습니다.")
        return

    today_str = datetime.today().strftime("%Y%m%d")
    filename = f"{base_filename}_{today_str}.csv"

    keys = data[0].keys()
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"[Saved] {filename} 파일이 생성되었습니다.")
    except Exception as e:
        print(f"[Error] CSV 저장 중 오류: {e}")
