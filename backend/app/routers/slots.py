from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from ..core.security import get_current_user
from ..models.user import UserPublic
from ..services.slot import SlotService

router = APIRouter(tags=["slots"])


def get_slot_service() -> SlotService:
    return SlotService()


@router.get("/slots/available")
async def available_slots(
    _: Annotated[UserPublic, Depends(get_current_user)],
    service: Annotated[SlotService, Depends(get_slot_service)],
    date: str = Query(..., description="YYYY-MM-DD"),
    category: str = Query(...),
):
    try:
        dt = datetime.fromisoformat(date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid date format") from exc
    slots = await service.available_slots(date=dt, category=category)
    return slots
