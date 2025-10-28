from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)


class MongoDocument(BaseModel):
    id: str | None = Field(
        default=None,
        alias="_id",
        serialization_alias="id",
        validation_alias="id",
    )
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = dict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class Pagination(BaseModel):
    total: int
    limit: int
    skip: int


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    pagination: Pagination


class ServiceResult(BaseModel):
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None