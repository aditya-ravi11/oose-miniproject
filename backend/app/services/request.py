"""Request service."""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.request import (
    CancelRequestPayload,
    PickupRequestCreate,
    PickupRequestPublic,
    RequestFilterParams,
    RequestStatus,
    SlotConfirmation,
)
from ..repositories.request import RequestRepository
from .notification import NotificationService
from .reward import RewardService

ALLOWED_CANCEL_STATUSES = {"draft", "submitted", "scheduled"}
ORDERED_STATUSES: dict[str, set[str]] = {
    "draft": {"submitted"},
    "submitted": {"pending_review", "cancelled"},
    "pending_review": {"scheduled", "cancelled"},
    "scheduled": {"enroute", "cancelled"},
    "enroute": {"onsite", "failed"},
    "onsite": {"collecting", "failed"},
    "collecting": {"collected", "failed"},
    "collected": {"handover"},
    "handover": {"verification"},
    "verification": {"completed"},
}


class RequestService:
    """Service for pickup request operations."""

    def __init__(self):
        self.repo = RequestRepository()
        self.notification_service = NotificationService()
        self.reward_service = RewardService()

    async def create(self, session: AsyncSession, user_id: int, payload: PickupRequestCreate) -> PickupRequestPublic:
        """Create a new pickup request."""
        data = payload.model_dump()
        data.update(
            {
                "user_id": user_id,
                "status": "submitted",
                "events": [
                    {
                        "type": "STATUS_CHANGE",
                        "at": datetime.utcnow().isoformat(),
                        "by": str(user_id),
                        "data": {"status": "submitted"},
                    }
                ],
            }
        )
        request = await self.repo.create(session, data)

        await self.notification_service.queue_notification(
            session,
            user_id=user_id,
            channel="email",
            title="Pickup request submitted",
            body=f"Your request {request.id} is submitted",
            meta={"request_id": request.id},
        )
        await self.notification_service.queue_notification(
            session,
            user_id=user_id,
            channel="inapp",
            title="Request submitted",
            body="We received your pickup request",
            meta={"request_id": request.id},
        )
        return request.to_public()

    async def list(self, session: AsyncSession, user_id: int, filters: RequestFilterParams) -> dict:
        """List pickup requests for a user."""
        query = {}
        if filters.status:
            query["status"] = filters.status
        if filters.category:
            query["category"] = filters.category

        docs, total = await self.repo.list_by_user(session, user_id, query, filters.skip, filters.limit)
        return {
            "items": [doc.to_public() for doc in docs],
            "total": total,
            "skip": filters.skip,
            "limit": filters.limit,
        }

    async def get(self, session: AsyncSession, request_id: int, user_id: int) -> PickupRequestPublic:
        """Get a single pickup request."""
        request = await self.repo.get(session, request_id, user_id)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        return request.to_public()

    async def cancel(
        self, session: AsyncSession, request_id: int, user_id: int, payload: CancelRequestPayload | None
    ) -> PickupRequestPublic:
        """Cancel a pickup request."""
        request = await self.repo.get(session, request_id, user_id)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

        if request.status not in ALLOWED_CANCEL_STATUSES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot cancel in current status")

        # Check 24h rule for scheduled requests
        if request.assigned_slot_json:
            import json

            assigned_slot = json.loads(request.assigned_slot_json)
            slot_start = assigned_slot.get("start")
            if slot_start:
                if isinstance(slot_start, str):
                    slot_start = datetime.fromisoformat(slot_start)
                if slot_start - datetime.now(timezone.utc) < timedelta(hours=24):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Too late to cancel (<24h)")

        updated = await self.repo.update(session, request_id, {"status": "cancelled"})
        await self.repo.append_event(
            session,
            request_id,
            {
                "type": "STATUS_CHANGE",
                "at": datetime.utcnow().isoformat(),
                "by": str(user_id),
                "data": {"from": request.status, "to": "cancelled", "reason": payload.reason if payload else None},
            },
        )
        return updated.to_public()

    async def confirm_slot(
        self, session: AsyncSession, request_id: int, user_id: int, slot: SlotConfirmation
    ) -> PickupRequestPublic:
        """Confirm a time slot for a pickup request."""
        request = await self.repo.get(session, request_id, user_id)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

        assigned_slot = {"start": slot.slot_start.isoformat(), "end": slot.slot_end.isoformat()}
        updated = await self.repo.update(session, request_id, {"assigned_slot": assigned_slot, "status": "scheduled"})

        await self.repo.append_event(
            session,
            request_id,
            {
                "type": "STATUS_CHANGE",
                "at": datetime.utcnow().isoformat(),
                "by": str(user_id),
                "data": {"from": request.status, "to": "scheduled"},
            },
        )

        await self.notification_service.queue_notification(
            session, user_id=user_id, channel="email", title="Pickup scheduled", body="Your slot is confirmed", meta={"request_id": request_id}
        )
        return updated.to_public()

    async def transition(
        self, session: AsyncSession, request_id: int, target_status: RequestStatus, actor: str = "system"
    ) -> PickupRequestPublic:
        """Transition a request to a new status."""
        request = await self.repo.get(session, request_id)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

        current = request.status
        allowed = ORDERED_STATUSES.get(current, set())
        if target_status not in allowed and target_status not in {"cancelled", "failed"}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transition")

        updated = await self.repo.update(session, request_id, {"status": target_status})
        await self.repo.append_event(
            session,
            request_id,
            {
                "type": "STATUS_CHANGE",
                "at": datetime.utcnow().isoformat(),
                "by": actor,
                "data": {"from": current, "to": target_status},
            },
        )

        if target_status == "completed":
            await self.reward_service.handle_completion(session, updated)

        return updated.to_public()
