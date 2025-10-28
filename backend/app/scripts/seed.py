"""Seed script for initial data."""
import asyncio
import json
from pathlib import Path

from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.security import hash_password
from ..db.engine import async_session_maker
from ..models.user import UserDB

ROOT = Path(__file__).resolve().parents[3]
USERS_FILE = ROOT / "infra" / "seed" / "seed_users.json"


async def seed() -> None:
    """Seed initial data."""
    async with async_session_maker() as session:
        if USERS_FILE.exists():
            users = json.loads(USERS_FILE.read_text())
            for user in users:
                # Check if user already exists
                from sqlmodel import select

                statement = select(UserDB).where(UserDB.email == user["email"])
                result = await session.exec(statement)
                existing = result.first()

                if existing:
                    print(f"User {user['email']} already exists, skipping")
                    continue

                user_db = UserDB(
                    name=user["name"],
                    email=user["email"],
                    phone=user.get("phone"),
                    password_hash=hash_password(user["password"]),
                    role="citizen",
                )
                session.add(user_db)

            await session.commit()
            print("✅ Seed data inserted successfully")


if __name__ == "__main__":
    asyncio.run(seed())
