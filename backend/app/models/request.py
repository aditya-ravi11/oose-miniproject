import json
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, JSON, String, Text
from sqlmodel import Field as SQLField, SQLModel

RequestStatus = Literal[
    "draft",
    "submitted",
    "pending_review",
    "scheduled",
    "enroute",
    "onsite",
    "collecting",
    "collected",
    "handover",
    "verification",
    "completed",
    "cancelled",
    "failed",
]


class Address(BaseModel):
    """Address schema."""

    line1: str
    line2: Optional[str] = None
    city: str
    pincode: str
    lat: Optional[float] = None
    lng: Optional[float] = None


class SlotWindow(BaseModel):
    """Time slot window schema."""

    start: datetime
    end: datetime


class RequestEvent(BaseModel):
    """Request event schema."""

    type: Literal["STATUS_CHANGE", "NOTE", "AUDIT"]
    at: datetime
    by: str
    data: Optional[dict[str, Any]] = None


class PickupRequestCreate(BaseModel):
    """Schema for creating a pickup request."""

    category: Literal["organic", "recyclable", "hazardous", "e-waste", "bulk", "other"]
    is_special: bool = False
    description: str
    quantity: float = Field(gt=0)
    address: Address
    preferred_slots: list[SlotWindow]
    photos: list[str] = []


class PickupRequestPublic(BaseModel):
    """Public pickup request schema (for responses)."""

    id: int
    user_id: int
    category: str
    is_special: bool = False
    description: str
    quantity: float
    photos: list[str]
    address: Address
    preferred_slots: list[SlotWindow]
    assigned_slot: Optional[SlotWindow] = None
    vendor_id: Optional[int] = None
    status: RequestStatus = "draft"
    events: list[RequestEvent] = []
    reward_points: int = 0
    created_at: datetime
    updated_at: datetime


class SlotConfirmation(BaseModel):
    """Schema for confirming a time slot."""

    slot_start: datetime
    slot_end: datetime


class RequestFilterParams(BaseModel):
    """Filter parameters for listing requests."""

    status: Optional[RequestStatus] = None
    category: Optional[str] = None
    skip: int = 0
    limit: int = 20


class CancelRequestPayload(BaseModel):
    """Payload for canceling a request."""

    reason: Optional[str] = None


class PickupRequestDB(SQLModel, table=True):
    """Pickup request database model (SQLModel table)."""

    __tablename__ = "pickup_requests"

    id: Optional[int] = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(foreign_key="users.id", index=True)
    category: str = SQLField(max_length=50)
    is_special: bool = SQLField(default=False)
    description: str = SQLField(sa_column=Column(Text))
    quantity: float
    photos_json: str = SQLField(sa_column=Column(Text, default="[]"))  # JSON array as string
    address_json: str = SQLField(sa_column=Column(Text))  # JSON object as string
    preferred_slots_json: str = SQLField(sa_column=Column(Text, default="[]"))  # JSON array
    assigned_slot_json: Optional[str] = SQLField(sa_column=Column(Text, nullable=True, default=None))  # JSON object
    vendor_id: Optional[int] = SQLField(default=None, foreign_key="users.id")
    status: str = SQLField(max_length=50, default="draft", index=True)
    events_json: str = SQLField(sa_column=Column(Text, default="[]"))  # JSON array
    reward_points: int = SQLField(default=0)
    created_at: datetime = SQLField(sa_column=Column(DateTime, nullable=False, default=datetime.utcnow))
    updated_at: datetime = SQLField(
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    def to_public(self) -> PickupRequestPublic:
        """Convert DB model to public schema."""
        return PickupRequestPublic(
            id=self.id,
            user_id=self.user_id,
            category=self.category,
            is_special=self.is_special,
            description=self.description,
            quantity=self.quantity,
            photos=json.loads(self.photos_json) if self.photos_json else [],
            address=Address(**json.loads(self.address_json)) if self.address_json else None,
            preferred_slots=[
                SlotWindow(**slot) for slot in json.loads(self.preferred_slots_json)
            ] if self.preferred_slots_json else [],
            assigned_slot=SlotWindow(**json.loads(self.assigned_slot_json)) if self.assigned_slot_json else None,
            vendor_id=self.vendor_id,
            status=self.status,
            events=[
                RequestEvent(**event) for event in json.loads(self.events_json)
            ] if self.events_json else [],
            reward_points=self.reward_points,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
