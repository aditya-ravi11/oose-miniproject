from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from ..core.security import get_current_user
from ..models.files import FileUploadResponse
from ..models.user import UserPublic
from ..services.storage import StorageService

router = APIRouter(prefix="/files", tags=["files"])


def get_storage_service() -> StorageService:
    return StorageService()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    _: Annotated[UserPublic, Depends(get_current_user)],
    storage: Annotated[StorageService, Depends(get_storage_service)],
    file: UploadFile = File(...),
):
    saved = await storage.save(file)
    return FileUploadResponse(**saved)
