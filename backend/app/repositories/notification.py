"""Notification repository using SQLModel."""
import json
from datetime import datetime
from typing import Optional

from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.notification import NotificationDB


class NotificationRepository:
    """Repository for notification operations."""

    async def queue(self, session: AsyncSession, data: dict) -> NotificationDB:
        """Queue a new notification."""
        # Convert meta dict to JSON string
        if "meta" in data:
            data["meta_json"] = json.dumps(data.pop("meta"))

        data.setdefault("status", "queued")
        notification = NotificationDB(**data)
        session.add(notification)
        await session.commit()
        await session.refresh(notification)
        return notification

    async def find_queued(self, session: AsyncSession, limit: int = 50) -> list[NotificationDB]:
        """Find queued notifications."""
        statement = select(NotificationDB).where(NotificationDB.status == "queued").limit(limit)
        result = await session.exec(statement)
        return list(result.all())

    async def mark_sent(self, session: AsyncSession, notif_id: int, success: bool) -> None:
        """Mark a notification as sent or failed."""
        notification = await session.get(NotificationDB, notif_id)
        if not notification:
            return

        notification.status = "sent" if success else "failed"
        notification.sent_at = datetime.utcnow()
        session.add(notification)
        await session.commit()

    async def list_by_user(self, session: AsyncSession, user_id: int, limit: int = 50) -> list[NotificationDB]:
        """List notifications for a user."""
        statement = (
            select(NotificationDB)
            .where(NotificationDB.user_id == user_id)
            .order_by(col(NotificationDB.created_at).desc())
            .limit(limit)
        )
        result = await session.exec(statement)
        return list(result.all())
