from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..core.security import get_current_user
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
):
    return await service.create(current_user.id, payload)


@router.get("")
async def list_requests(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
    status: str | None = Query(default=None),
    category: str | None = Query(default=None),
    skip: int = 0,
    limit: int = 20,
):
    filters = RequestFilterParams(status=status, category=category, skip=skip, limit=limit)
    return await service.list(current_user.id, filters)


@router.get("/{request_id}")
async def get_request(
    request_id: str,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
):
    return await service.get(request_id, current_user.id)


@router.post("/{request_id}/cancel")
async def cancel_request(
    request_id: str,
    payload: CancelRequestPayload | None,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
):
    return await service.cancel(request_id, current_user.id, payload)


@router.post("/{request_id}/confirm-slot")
async def confirm_slot(
    request_id: str,
    payload: SlotConfirmation,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[RequestService, Depends(get_request_service)],
):
    return await service.confirm_slot(request_id, current_user.id, payload)
