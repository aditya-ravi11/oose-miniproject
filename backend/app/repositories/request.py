"""Request repository using SQLModel."""
import json
from datetime import datetime
from typing import Optional

from sqlmodel import col, delete, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.request import PickupRequestDB


class RequestRepository:
    """Repository for pickup request operations."""

    async def create(self, session: AsyncSession, data: dict) -> PickupRequestDB:
        """Create a new pickup request."""
        # Convert complex fields to JSON strings
        if "address" in data:
            data["address_json"] = json.dumps(data.pop("address").model_dump() if hasattr(data["address"], "model_dump") else data["address"])
        if "preferred_slots" in data:
            slots = data.pop("preferred_slots")
            data["preferred_slots_json"] = json.dumps([s.model_dump() if hasattr(s, "model_dump") else s for s in slots])
        if "photos" in data:
            data["photos_json"] = json.dumps(data.pop("photos"))
        if "events" in data:
            events = data.pop("events")
            data["events_json"] = json.dumps([e.model_dump() if hasattr(e, "model_dump") else e for e in events])

        request = PickupRequestDB(**data)
        session.add(request)
        await session.commit()
        await session.refresh(request)
        return request

    async def list_by_user(
        self, session: AsyncSession, user_id: int, filters: dict, skip: int, limit: int
    ) -> tuple[list[PickupRequestDB], int]:
        """List requests for a user with filters."""
        statement = select(PickupRequestDB).where(PickupRequestDB.user_id == user_id)

        if "status" in filters:
            statement = statement.where(PickupRequestDB.status == filters["status"])
        if "category" in filters:
            statement = statement.where(PickupRequestDB.category == filters["category"])

        # Get total count
        count_statement = select(func.count()).select_from(PickupRequestDB).where(PickupRequestDB.user_id == user_id)
        if "status" in filters:
            count_statement = count_statement.where(PickupRequestDB.status == filters["status"])
        if "category" in filters:
            count_statement = count_statement.where(PickupRequestDB.category == filters["category"])

        total_result = await session.exec(count_statement)
        total = total_result.one()

        # Get paginated results
        statement = statement.order_by(col(PickupRequestDB.created_at).desc()).offset(skip).limit(limit)
        result = await session.exec(statement)
        docs = result.all()
        return list(docs), total

    async def get(self, session: AsyncSession, request_id: int, user_id: Optional[int] = None) -> Optional[PickupRequestDB]:
        """Get a request by ID, optionally filtered by user."""
        statement = select(PickupRequestDB).where(PickupRequestDB.id == request_id)
        if user_id:
            statement = statement.where(PickupRequestDB.user_id == user_id)
        result = await session.exec(statement)
        return result.first()

    async def update(self, session: AsyncSession, request_id: int, payload: dict) -> Optional[PickupRequestDB]:
        """Update a request."""
        request = await session.get(PickupRequestDB, request_id)
        if not request:
            return None

        # Handle JSON fields
        if "assigned_slot" in payload:
            slot = payload.pop("assigned_slot")
            payload["assigned_slot_json"] = json.dumps(slot.model_dump() if hasattr(slot, "model_dump") else slot) if slot else None

        # Update fields
        for key, value in payload.items():
            setattr(request, key, value)

        request.updated_at = datetime.utcnow()
        session.add(request)
        await session.commit()
        await session.refresh(request)
        return request

    async def append_event(self, session: AsyncSession, request_id: int, event: dict) -> None:
        """Append an event to a request."""
        request = await session.get(PickupRequestDB, request_id)
        if not request:
            return

        events = json.loads(request.events_json) if request.events_json else []
        # Serialize datetime objects
        if "at" in event and isinstance(event["at"], datetime):
            event["at"] = event["at"].isoformat()
        events.append(event)
        request.events_json = json.dumps(events)
        request.updated_at = datetime.utcnow()
        session.add(request)
        await session.commit()

    async def mark_reward(self, session: AsyncSession, request_id: int, points: int) -> None:
        """Mark reward points for a request."""
        request = await session.get(PickupRequestDB, request_id)
        if not request:
            return

        request.reward_points += points
        request.updated_at = datetime.utcnow()
        session.add(request)
        await session.commit()

    async def find_conflicting_slots(self, session: AsyncSession, day_start: datetime, day_end: datetime) -> list[PickupRequestDB]:
        """Find requests with assigned slots in a given time range."""
        # Note: Since assigned_slot is JSON, we can't do efficient date range queries
        # We'll fetch all scheduled requests and filter in Python
        statement = select(PickupRequestDB).where(
            PickupRequestDB.status.notin_(["cancelled", "failed"]),
            PickupRequestDB.assigned_slot_json.isnot(None)
        )
        result = await session.exec(statement)
        requests = result.all()

        # Filter by date range in Python
        filtered = []
        for req in requests:
            if req.assigned_slot_json:
                slot = json.loads(req.assigned_slot_json)
                slot_start = datetime.fromisoformat(slot["start"]) if isinstance(slot["start"], str) else slot["start"]
                if day_start <= slot_start < day_end:
                    filtered.append(req)

        return filtered

    async def cleanup_drafts(self, session: AsyncSession, older_than: datetime) -> int:
        """Delete draft requests older than a given date."""
        statement = delete(PickupRequestDB).where(
            PickupRequestDB.status == "draft",
            PickupRequestDB.created_at < older_than
        )
        result = await session.exec(statement)
        await session.commit()
        return result.rowcount
