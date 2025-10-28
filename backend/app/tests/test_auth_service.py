import pytest
from fastapi import HTTPException

from app.models.user import UserCreate
from app.services.auth import AuthService


class FakeUserRepo:
    def __init__(self) -> None:
        self.users: dict[str, dict] = {}

    async def get_by_email(self, email: str):
        return self.users.get(email)

    async def create(self, data: dict):
        identifier = str(len(self.users) + 1)
        stored = {"_id": identifier, **data}
        self.users[data["email"]] = stored
        self.users[identifier] = stored
        return stored

    async def get_by_id(self, identifier: str):
        return self.users.get(identifier)


@pytest.mark.anyio
async def test_register_and_login_roundtrip():
    repo = FakeUserRepo()
    service = AuthService(repo)
    payload = UserCreate(name="Citizen", email="c@example.com", phone="123", password="secret")

    token = await service.register(payload)
    assert token.user.email == payload.email

    login_resp = await service.login(payload.email, payload.password)
    assert login_resp.user.email == payload.email
    assert login_resp.access_token


@pytest.mark.anyio
async def test_login_invalid_credentials():
    repo = FakeUserRepo()
    service = AuthService(repo)
    payload = UserCreate(name="Citizen", email="c2@example.com", phone="123", password="secret")
    await service.register(payload)

    with pytest.raises(HTTPException):
        await service.login(payload.email, "wrong")