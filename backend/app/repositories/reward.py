"""Reward repository using SQLModel."""
from sqlmodel import col, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.reward import RewardDB


class RewardRepository:
    """Repository for reward operations."""

    async def grant(self, session: AsyncSession, data: dict) -> RewardDB:
        """Grant a new reward."""
        reward = RewardDB(**data)
        session.add(reward)
        await session.commit()
        await session.refresh(reward)
        return reward

    async def list_recent(self, session: AsyncSession, user_id: int, limit: int = 10) -> list[RewardDB]:
        """List recent rewards for a user."""
        statement = (
            select(RewardDB)
            .where(RewardDB.user_id == user_id)
            .order_by(col(RewardDB.created_at).desc())
            .limit(limit)
        )
        result = await session.exec(statement)
        return list(result.all())

    async def total_points(self, session: AsyncSession, user_id: int) -> int:
        """Calculate total reward points for a user."""
        statement = select(func.sum(RewardDB.points)).where(RewardDB.user_id == user_id)
        result = await session.exec(statement)
        total = result.one()
        return int(total) if total else 0
