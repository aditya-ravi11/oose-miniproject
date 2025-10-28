"""User repository using SQLModel."""
from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.user import UserDB


class UserRepository:
    """Repository for user operations."""

    async def create(self, session: AsyncSession, data: dict) -> UserDB:
        """Create a new user."""
        user = UserDB(**data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UserDB]:
        """Get user by email."""
        statement = select(UserDB).where(UserDB.email == email)
        result = await session.exec(statement)
        return result.first()

    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional[UserDB]:
        """Get user by ID."""
        return await session.get(UserDB, user_id)
