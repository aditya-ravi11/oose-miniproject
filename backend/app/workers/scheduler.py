"""Background scheduler for periodic tasks."""
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..db.engine import async_session_maker
from ..repositories.request import RequestRepository
from ..services.notification import NotificationService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def cleanup_drafts() -> None:
    """Clean up old draft requests (older than 7 days)."""
    async with async_session_maker() as session:
        repo = RequestRepository()
        threshold = datetime.utcnow() - timedelta(days=7)
        deleted = await repo.cleanup_drafts(session, threshold)
        if deleted:
            logger.info("Cleaned %s expired drafts", deleted)


async def process_notifications() -> None:
    """Process queued notifications."""
    service = NotificationService()
    await service.process_queue()


def init_scheduler() -> None:
    """Initialize and start the background scheduler."""
    if scheduler.running:
        return
    scheduler.add_job(cleanup_drafts, "cron", hour=3)
    scheduler.add_job(process_notifications, "interval", minutes=2)
    scheduler.start()
    logger.info("APScheduler started")
