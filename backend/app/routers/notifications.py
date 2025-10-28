"""Notifications router."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.security import get_current_user
from ..db.engine import get_session
from ..models.user import UserPublic
from ..repositories.notification import NotificationRepository

router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notification_repository() -> NotificationRepository:
    return NotificationRepository()


@router.get("")
async def list_notifications(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    repo: Annotated[NotificationRepository, Depends(get_notification_repository)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """List notifications for current user."""
    docs = await repo.list_by_user(session, current_user.id)
    return [doc.to_public() for doc in docs]
