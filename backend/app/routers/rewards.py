"""Rewards router."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.security import get_current_user
from ..db.engine import get_session
from ..models.user import UserPublic
from ..services.reward import RewardService

router = APIRouter(prefix="/rewards", tags=["rewards"])


def get_reward_service() -> RewardService:
    return RewardService()


@router.get("/summary")
async def summary(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RewardService, Depends(get_reward_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Get reward summary for current user."""
    return await service.summary(session, current_user.id)
