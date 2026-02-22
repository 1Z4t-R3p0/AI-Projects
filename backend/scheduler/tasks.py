from apscheduler.schedulers.background import BackgroundScheduler
import datetime

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(check_reminders, 'interval', minutes=60)
    scheduler.start()

def check_reminders():
    print(f"[{datetime.datetime.now()}] Checking for active user reminders...")
    # SQL query to find due reminders would go here
