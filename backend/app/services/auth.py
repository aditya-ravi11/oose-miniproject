"""Authentication service."""
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.security import create_access_token, hash_password, verify_password
from ..models.user import TokenResponse, UserCreate, UserPublic
from ..repositories.user import UserRepository


class AuthService:
    """Service for authentication operations."""

    def __init__(self):
        self.repo = UserRepository()

    async def register(self, session: AsyncSession, payload: UserCreate) -> TokenResponse:
        """Register a new user."""
        existing = await self.repo.get_by_email(session, payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        data = payload.model_dump()
        data["password_hash"] = hash_password(payload.password)
        data.pop("password")
        data["role"] = "citizen"

        user = await self.repo.create(session, data)
        token = create_access_token(str(user.id))
        return TokenResponse(access_token=token, user=user.to_public())

    async def login(self, session: AsyncSession, email: str, password: str) -> TokenResponse:
        """Login a user."""
        user = await self.repo.get_by_email(session, email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(str(user.id))
        return TokenResponse(access_token=token, user=user.to_public())

    async def me(self, session: AsyncSession, user_id: int) -> UserPublic:
        """Get current user profile."""
        user = await self.repo.get_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user.to_public()
