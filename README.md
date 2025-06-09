# kiwoom_auto_trading_with_selector

Daily selector that gathers KOSPI stock prices, computes MA20/MA50 and RSI(14),
and groups stocks into A/B/C buy candidates. The results are saved to
`candidates_YYYYMMDD.csv` after market close.

## Setup

1. **Python 3.8+** is required.
2. *(Optional)* create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Kiwoom credentials

`KiwoomAPI.login()` automatically loads a `.env` file (if found) and reads
`KIWOOM_USER` and `KIWOOM_PW` from the environment before connecting. Set these
variables in your shell or in a `.env` file:

```
KIWOOM_USER=your_id
KIWOOM_PW=your_password
```

## Usage

Run the full workflow manually with:

```bash
python main.py
```

It logs in, collects recent price data, computes indicators and saves a CSV
containing today’s candidates.

## Scheduler

`scheduler.py` uses APScheduler to invoke `main.main()` once per weekday after
the Korean market closes. Start it with:

```bash
python scheduler.py
```

The job runs at **16:05 KST** Monday through Friday until stopped.
