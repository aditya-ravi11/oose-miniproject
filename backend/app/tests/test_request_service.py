from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.models.request import CancelRequestPayload
from app.services.request import RequestService


class FakeNotificationService:
    async def queue_notification(self, **_):
        return {}


class FakeRewardService:
    async def handle_completion(self, *_):
        return None


class FakeRequestRepo:
    def __init__(self):
        future = datetime.now(timezone.utc) + timedelta(days=2)
        base_request = {
            "category": "recyclable",
            "description": "Old newspapers",
            "quantity": 3,
            "photos": [],
            "address": {"line1": "123", "city": "Mumbai", "pincode": "400077"},
            "preferred_slots": [],
        }
        self.requests = {
            "1": {
                "_id": "1",
                "user_id": "user",
                "status": "scheduled",
                **base_request,
                "assigned_slot": {"start": future.isoformat(), "end": (future + timedelta(hours=1)).isoformat()},
                "events": [],
            },
            "2": {
                "_id": "2",
                "user_id": "user",
                "status": "scheduled",
                **base_request,
                "assigned_slot": {
                    "start": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
                    "end": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
                },
                "events": [],
            },
        }

    async def create(self, data):
        identifier = str(len(self.requests) + 1)
        data["_id"] = identifier
        self.requests[identifier] = data
        return data

    async def list_by_user(self, *args, **kwargs):
        return list(self.requests.values()), len(self.requests)

    async def get(self, request_id, user_id=None):
        req = self.requests.get(request_id)
        if user_id and req and req["user_id"] != user_id:
            return None
        return req

    async def update(self, request_id, payload):
        self.requests[request_id].update(payload)
        return self.requests[request_id]

    async def append_event(self, request_id, event):
        self.requests[request_id].setdefault("events", []).append(event)


@pytest.mark.anyio
async def test_cancel_request_honors_time_window():
    service = RequestService(
        repo=FakeRequestRepo(),
        notification_service=FakeNotificationService(),
        reward_service=FakeRewardService(),
    )
    cancelled = await service.cancel("1", "user", CancelRequestPayload(reason="change"))
    assert cancelled.status == "cancelled"

    with pytest.raises(HTTPException):
        await service.cancel("2", "user", CancelRequestPayload(reason="late"))
