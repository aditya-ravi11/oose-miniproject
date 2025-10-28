from typing import Annotated

from fastapi import APIRouter, Depends

from ..core.security import get_current_user
from ..models.notification import NotificationPublic
from ..models.user import UserPublic
from ..repositories.notification import NotificationRepository

router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notification_repository() -> NotificationRepository:
    return NotificationRepository()


@router.get("")
async def list_notifications(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    repo: Annotated[NotificationRepository, Depends(get_notification_repository)],
):
    docs = await repo.list_by_user(current_user.id)
    return [NotificationPublic(**doc) for doc in docs]
