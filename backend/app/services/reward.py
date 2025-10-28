"""Reward service."""
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.reward import RewardPublic
from ..repositories.request import RequestRepository
from ..repositories.reward import RewardRepository


class RewardService:
    """Service for reward operations."""

    def __init__(self):
        self.reward_repo = RewardRepository()
        self.request_repo = RequestRepository()

    async def handle_completion(self, session: AsyncSession, request) -> None:
        """Handle reward on request completion."""
        category = request.category
        points = 5 if category == "recyclable" else 10 if category in {"e-waste", "hazardous"} else 0
        if points <= 0:
            return

        await self.reward_repo.grant(
            session,
            {
                "user_id": request.user_id,
                "points": points,
                "reason": f"Completed {category} pickup",
            },
        )
        await self.request_repo.mark_reward(session, request.id, points)

    async def summary(self, session: AsyncSession, user_id: int) -> dict:
        """Get reward summary for a user."""
        total = await self.reward_repo.total_points(session, user_id)
        recent_docs = await self.reward_repo.list_recent(session, user_id)
        return {
            "total_points": total,
            "recent": [doc.to_public() for doc in recent_docs],
        }
