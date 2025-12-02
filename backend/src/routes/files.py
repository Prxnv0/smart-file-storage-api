from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, status

from src.config import settings
from src.services.metadata import FileMetadataService
from src.services.storage import LocalStorageService
from src.services.storage_s3 import S3StorageService

router = APIRouter(prefix="/files", tags=["files"])


# Initialize services (for now simple instances; can be wired via DI later)
metadata_service = FileMetadataService()

if settings.STORAGE_BACKEND.lower() == "s3":
    storage_service = S3StorageService()
else:
    storage_service = LocalStorageService()


@router.get("", summary="List uploaded files")
async def list_files() -> List[dict]:
    """Return list of stored file metadata.

    For now this uses an in-memory store and local disk paths.
    Later this will be backed by Postgres + S3.
    """
    return metadata_service.list_files()


@router.post(
    "/upload",
    summary="Upload a file",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(file: UploadFile = File(...)) -> dict:
    """Upload a file and store it on local disk for now.

    - File bytes are written under a configurable local upload directory.
    - Basic metadata is stored via the metadata service.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    saved_path = await storage_service.save_file(file)
    metadata = metadata_service.add_file(
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        storage_path=str(saved_path),
    )
    return {"message": "File uploaded", "file": metadata}
