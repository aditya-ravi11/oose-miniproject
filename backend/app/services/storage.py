import os
import uuid
from datetime import datetime
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from slugify import slugify

from ..core.config import get_settings


class StorageService:
    def __init__(self) -> None:
        settings = get_settings()
        self.upload_dir = Path(settings.upload_dir)
        self.base_url = settings.storage_base_url.rstrip("/")

    async def save(self, file: UploadFile) -> dict:
        timestamp = datetime.utcnow()
        relative = Path(str(timestamp.year), f"{timestamp.month:02d}")
        stem = slugify(Path(file.filename or "file").stem)
        ext = Path(file.filename or "").suffix or ".bin"
        name = f"{stem}-{uuid.uuid4().hex}{ext}"
        destination = self.upload_dir / relative
        os.makedirs(destination, exist_ok=True)
        full_path = destination / name
        async with aiofiles.open(full_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                await buffer.write(chunk)
        relative_path = relative / name
        url = f"{self.base_url}/uploads/{relative_path.as_posix()}"
        return {"url": url, "path": str(relative_path)}