"""Scheduler setup for daily job"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo

import main


def start():
    """Start APScheduler that runs main.main() each weekday after market close."""
    tz = ZoneInfo("Asia/Seoul")
    scheduler = BlockingScheduler(timezone=tz)
    # Run at 16:05 Korea time Monday through Friday
    trigger = CronTrigger(day_of_week="mon-fri", hour=16, minute=5, timezone=tz)
    scheduler.add_job(main.main, trigger)
    print("[Scheduler] Initialized. Waiting for daily job at 16:05 KST.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    start()
