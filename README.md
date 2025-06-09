# kiwoom_auto_trading_with_selector

kiwoom_auto_trading_with_selector

## Scheduler

`scheduler.py` uses APScheduler to invoke `main.main()` once per weekday after the Korean market closes.
Run the scheduler with:

```bash
python scheduler.py
```

The job is scheduled at **16:05 KST** Monday through Friday and will keep running until stopped.
