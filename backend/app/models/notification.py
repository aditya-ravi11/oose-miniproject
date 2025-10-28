import json
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Text
from sqlmodel import Field as SQLField, SQLModel


class NotificationCreate(BaseModel):
    """Schema for creating a notification."""

    user_id: int
    channel: Literal["email", "sms", "push", "inapp"] = "email"
    title: str
    body: str
    meta: Optional[dict] = None


class NotificationPublic(BaseModel):
    """Public notification schema (for responses)."""

    id: int
    user_id: int
    channel: str
    title: str
    body: str
    meta: Optional[dict] = None
    status: Literal["queued", "sent", "failed"] = "queued"
    sent_at: Optional[datetime] = None
    created_at: datetime


class NotificationDB(SQLModel, table=True):
    """Notification database model (SQLModel table)."""

    __tablename__ = "notifications"

    id: Optional[int] = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(foreign_key="users.id", index=True)
    channel: str = SQLField(max_length=50)
    title: str = SQLField(max_length=255)
    body: str = SQLField(sa_column=Column(Text))
    meta_json: str = SQLField(sa_column=Column(Text, default="{}"))  # JSON object as string
    status: str = SQLField(max_length=50, default="queued")
    sent_at: Optional[datetime] = SQLField(sa_column=Column(DateTime, nullable=True, default=None))
    created_at: datetime = SQLField(sa_column=Column(DateTime, nullable=False, default=datetime.utcnow))

    def to_public(self) -> NotificationPublic:
        """Convert DB model to public schema."""
        return NotificationPublic(
            id=self.id,
            user_id=self.user_id,
            channel=self.channel,
            title=self.title,
            body=self.body,
            meta=json.loads(self.meta_json) if self.meta_json else {},
            status=self.status,
            sent_at=self.sent_at,
            created_at=self.created_at,
        )
