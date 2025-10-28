from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Column, DateTime, Field as SQLField, SQLModel, String


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    name: str
    email: EmailStr
    phone: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """Public user schema (for responses)."""

    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = "citizen"


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class UserDB(SQLModel, table=True):
    """User database model (SQLModel table)."""

    __tablename__ = "users"

    id: Optional[int] = SQLField(default=None, primary_key=True)
    name: str = SQLField(max_length=255)
    email: str = SQLField(max_length=255, unique=True, index=True, sa_column_kwargs={"nullable": False})
    phone: Optional[str] = SQLField(max_length=50, default=None)
    password_hash: str = SQLField(max_length=255)
    role: str = SQLField(max_length=50, default="citizen")
    created_at: datetime = SQLField(
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = SQLField(
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    def to_public(self) -> UserPublic:
        """Convert DB model to public schema."""
        return UserPublic(
            id=self.id,
            name=self.name,
            email=self.email,
            phone=self.phone,
            role=self.role,
        )
