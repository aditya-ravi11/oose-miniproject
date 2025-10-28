"""Requests router."""
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.security import get_current_user
from ..db.engine import get_session
from ..models.request import (
    CancelRequestPayload,
    PickupRequestCreate,
    RequestFilterParams,
    SlotConfirmation,
)
from ..models.user import UserPublic
from ..services.request import RequestService

router = APIRouter(prefix="/requests", tags=["requests"])


def get_request_service() -> RequestService:
    return RequestService()


@router.post("", status_code=201)
async def create_request(
    payload: PickupRequestCreate,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Create a new pickup request."""
    return await service.create(session, current_user.id, payload)


@router.get("")
async def list_requests(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    status: str | None = Query(default=None),
    category: str | None = Query(default=None),
    skip: int = 0,
    limit: int = 20,
):
    """List pickup requests for current user."""
    filters = RequestFilterParams(status=status, category=category, skip=skip, limit=limit)
    return await service.list(session, current_user.id, filters)


@router.get("/{request_id}")
async def get_request(
    request_id: int,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Get a single pickup request."""
    return await service.get(session, request_id, current_user.id)


@router.post("/{request_id}/cancel")
async def cancel_request(
    request_id: int,
    payload: CancelRequestPayload | None,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Cancel a pickup request."""
    return await service.cancel(session, request_id, current_user.id, payload)


@router.post("/{request_id}/confirm-slot")
async def confirm_slot(
    request_id: int,
    payload: SlotConfirmation,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Confirm a time slot for pickup."""
    return await service.confirm_slot(session, request_id, current_user.id, payload)
