"""Authentication router."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.security import get_current_user
from ..db.engine import get_session
from ..models.user import TokenResponse, UserCreate, UserLogin, UserPublic
from ..services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service() -> AuthService:
    return AuthService()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    payload: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Register a new user."""
    return await service.register(session, payload)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: UserLogin,
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Login a user."""
    return await service.login(session, payload.email, payload.password)


@router.get("/me", response_model=UserPublic)
async def me(current_user: Annotated[UserPublic, Depends(get_current_user)]):
    """Get current user profile."""
    return current_user
