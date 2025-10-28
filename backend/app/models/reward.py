from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlmodel import Field as SQLField, SQLModel


class RewardGrant(BaseModel):
    """Schema for granting a reward."""

    user_id: int
    points: int
    reason: str


class RewardPublic(BaseModel):
    """Public reward schema (for responses)."""

    id: int
    user_id: int
    points: int
    reason: str
    created_at: datetime


class RewardSummary(BaseModel):
    """Reward summary schema."""

    total_points: int
    recent: list[RewardPublic]


class RewardDB(SQLModel, table=True):
    """Reward database model (SQLModel table)."""

    __tablename__ = "rewards"

    id: Optional[int] = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(foreign_key="users.id", index=True)
    points: int
    reason: str = SQLField(max_length=255)
    created_at: datetime = SQLField(sa_column=Column(DateTime, nullable=False, default=datetime.utcnow))

    def to_public(self) -> RewardPublic:
        """Convert DB model to public schema."""
        return RewardPublic(
            id=self.id,
            user_id=self.user_id,
            points=self.points,
            reason=self.reason,
            created_at=self.created_at,
        )
