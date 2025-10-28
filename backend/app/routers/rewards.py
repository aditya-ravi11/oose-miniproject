from typing import Annotated

from fastapi import APIRouter, Depends

from ..core.security import get_current_user
from ..models.user import UserPublic
from ..services.reward import RewardService

router = APIRouter(prefix="/rewards", tags=["rewards"])


def get_reward_service() -> RewardService:
    return RewardService()


@router.get("/summary")
async def summary(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RewardService, Depends(get_reward_service)],
):
    return await service.summary(current_user.id)
