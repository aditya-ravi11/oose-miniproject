"""Notification service."""
import asyncio
import logging
import smtplib
from email.message import EmailMessage

from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.config import get_settings
from ..db.engine import async_session_maker
from ..repositories.notification import NotificationRepository
from ..repositories.user import UserRepository
from .ws import manager

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for notification operations."""

    def __init__(self):
        self.repo = NotificationRepository()
        self.settings = get_settings()
        self.user_repo = UserRepository()

    async def queue_notification(
        self, session: AsyncSession, *, user_id: int, channel: str, title: str, body: str, meta: dict | None = None
    ) -> dict:
        """Queue a notification."""
        notification = await self.repo.queue(
            session,
            {
                "user_id": user_id,
                "channel": channel,
                "title": title,
                "body": body,
                "meta": meta or {},
                "status": "queued",
            },
        )
        if channel == "inapp":
            # Send immediately via WebSocket
            await manager.send(str(user_id), notification.to_public().model_dump())
            await self.repo.mark_sent(session, notification.id, True)
        return notification.to_public().model_dump()

    async def push_inapp(self, user_id: int, payload: dict) -> None:
        """Push an in-app notification."""
        await manager.send(str(user_id), payload)

    async def process_queue(self) -> None:
        """Process queued notifications (called by scheduler)."""
        async with async_session_maker() as session:
            queued = await self.repo.find_queued(session)
            for notification in queued:
                success = False
                try:
                    if notification.channel == "email":
                        success = await self._send_email(session, notification)
                    elif notification.channel == "sms":
                        success = self._send_sms_stub(notification)
                    elif notification.channel == "push":
                        success = self._send_push_stub(notification)
                except Exception as exc:
                    logger.exception("Failed to send notification %s: %s", notification.id, exc)
                finally:
                    await self.repo.mark_sent(session, notification.id, success)

    async def _send_email(self, session: AsyncSession, notification) -> bool:
        """Send email notification."""
        message = EmailMessage()
        message["From"] = self.settings.email_from

        # Get recipient email
        import json

        meta = json.loads(notification.meta_json) if notification.meta_json else {}
        recipient = meta.get("email") or meta.get("recipient")
        if not recipient:
            recipient_user = await self.user_repo.get_by_id(session, notification.user_id)
            recipient = recipient_user.email if recipient_user else None

        message["To"] = recipient
        if not message["To"]:
            logger.warning("Skipping email notification %s without recipient", notification.id)
            return False

        message["Subject"] = notification.title
        message.set_content(notification.body)

        def _send():
            with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port) as smtp:
                if self.settings.smtp_user:
                    smtp.login(self.settings.smtp_user, self.settings.smtp_pass)
                smtp.send_message(message)

        await asyncio.to_thread(_send)
        return True

    def _send_sms_stub(self, notification) -> bool:
        """SMS stub."""
        if not self.settings.enable_sms:
            logger.info("SMS disabled, skipping notification %s", notification.id)
            return False
        logger.info("[SMS] %s", notification)
        return True

    def _send_push_stub(self, notification) -> bool:
        """Push notification stub."""
        if not self.settings.enable_push:
            logger.info("Push disabled, skipping notification %s", notification.id)
            return False
        logger.info("[Push] %s", notification)
        return True
