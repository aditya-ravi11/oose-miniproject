from datetime import datetime

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from ..db.client import get_database


class BaseRepository:
    collection_name: str

    def __init__(self):
        db = get_database()
        self.collection: AsyncIOMotorCollection = db[self.collection_name]

    @staticmethod
    def to_object_id(value: str | ObjectId) -> ObjectId:
        return value if isinstance(value, ObjectId) else ObjectId(value)

    def stamp(self, payload: dict) -> dict:
        now = datetime.utcnow()
        payload.setdefault("created_at", now)
        payload["updated_at"] = now
        return payload