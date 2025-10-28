"""Application settings via pydantic-settings."""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class FeatureFlags(BaseModel):
    enable_sms: bool = False
    enable_push: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    api_port: int = Field(8000, alias="API_PORT")
    database_url: str = Field("sqlite+aiosqlite:///./data/swmra.db", alias="DATABASE_URL")

    jwt_secret: str = Field("devsecret_change_me", alias="JWT_SECRET")
    jwt_expire_min: int = Field(60, alias="JWT_EXPIRE_MIN")

    smtp_host: str = Field("smtp.mailtrap.io", alias="SMTP_HOST")
    smtp_port: int = Field(2525, alias="SMTP_PORT")
    smtp_user: str = Field("your_user", alias="SMTP_USER")
    smtp_pass: str = Field("your_pass", alias="SMTP_PASS")
    email_from: str = Field("no-reply@swmra.local", alias="EMAIL_FROM")

    enable_sms: bool = Field(False, alias="ENABLE_SMS")
    enable_push: bool = Field(False, alias="ENABLE_PUSH")

    rate_limit_per_min: int = Field(60, alias="RATE_LIMIT_PER_MIN")
    upload_dir: str = Field("uploads", alias="UPLOAD_DIR")
    storage_base_url: AnyHttpUrl | str = Field("http://localhost:8000", alias="STORAGE_BASE_URL")

    slot_capacity_per_day: int = Field(24, alias="SLOT_CAPACITY_PER_DAY")
    special_slot_capacity: int = Field(2, alias="SPECIAL_SLOT_CAPACITY")

    cors_origins: List[AnyHttpUrl | str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    scheduler_cleanup_cron: str = Field("0 2 * * *", alias="SCHEDULER_CLEANUP_CRON")
    scheduler_email_interval_seconds: int = Field(60, alias="SCHEDULER_EMAIL_INTERVAL")

    @property
    def feature_flags(self) -> FeatureFlags:
        return FeatureFlags(enable_sms=self.enable_sms, enable_push=self.enable_push)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
