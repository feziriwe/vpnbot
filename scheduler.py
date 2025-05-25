from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.db import delete_expired_keys

def start_scheduler(bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_expired_keys, "interval", hours=1)
    scheduler.start()