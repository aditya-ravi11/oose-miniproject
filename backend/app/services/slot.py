"""Slot service."""
import json
from datetime import datetime, time, timedelta
from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.config import get_settings
from ..repositories.request import RequestRepository


class SlotService:
    """Service for slot operations."""

    def __init__(self):
        self.repo = RequestRepository()
        self.settings = get_settings()

    async def available_slots(self, session: AsyncSession, *, date: datetime, category: str) -> List[dict]:
        """Get available slots for a given date and category."""
        base_date = date.date()
        day_start = datetime.combine(base_date, time(hour=9))
        day_end = datetime.combine(base_date, time(hour=21))
        slot_length = timedelta(minutes=60)
        slots: list[dict] = []

        assigned = await self.repo.find_conflicting_slots(session, day_start, day_end)
        taken = set()
        for item in assigned:
            if item.assigned_slot_json:
                slot = json.loads(item.assigned_slot_json)
                start = slot.get("start")
                end = slot.get("end")
                if start and end:
                    taken.add((start, end))

        capacity = self.settings.special_slot_capacity if category in {"hazardous", "e-waste"} else self.settings.slot_capacity_per_day
        current = day_start
        while current < day_end and len(slots) < capacity:
            slot = {"start": current.isoformat(), "end": (current + slot_length).isoformat()}
            if (slot["start"], slot["end"]) not in taken:
                slots.append(slot)
            current += slot_length

        return slots
