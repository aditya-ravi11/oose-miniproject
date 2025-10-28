from datetime import datetime, timedelta
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..repositories.request import RequestRepository
from ..services.notification import NotificationService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def cleanup_drafts() -> None:
    repo = RequestRepository()
    threshold = datetime.utcnow() - timedelta(days=7)
    deleted = await repo.cleanup_drafts(threshold)
    if deleted:
        logger.info("Cleaned %s expired drafts", deleted)


async def process_notifications() -> None:
    service = NotificationService()
    await service.process_queue()


def init_scheduler() -> None:
    if scheduler.running:
        return
    scheduler.add_job(cleanup_drafts, "cron", hour=3)
    scheduler.add_job(process_notifications, "interval", minutes=2)
    scheduler.start()
    logger.info("APScheduler started")