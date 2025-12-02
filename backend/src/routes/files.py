from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends

from src.config import settings
from src.db import get_db
from src.services.metadata_db import DbFileMetadataService
from src.services.storage import LocalStorageService
from src.services.storage_s3 import S3StorageService

router = APIRouter(prefix="/files", tags=["files"])


if settings.STORAGE_BACKEND.lower() == "s3":
    storage_service = S3StorageService()
else:
    storage_service = LocalStorageService()


@router.get("", summary="List uploaded files")
async def list_files(db=Depends(get_db)) -> List[dict]:
    """Return list of stored file metadata from the database."""
    metadata_service = DbFileMetadataService(db)
    return metadata_service.list_files()


@router.post(
    "/upload",
    summary="Upload a file",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(file: UploadFile = File(...), db=Depends(get_db)) -> dict:
    """Upload a file and store it on local disk for now.

    - File bytes are written under a configurable local upload directory.
    - Basic metadata is stored via the metadata service.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    saved_path = await storage_service.save_file(file)
    metadata_service = DbFileMetadataService(db)
    metadata = metadata_service.create_file(
        filename=file.filename,
        content_type=file.content_type,
        storage_path=str(saved_path),
        size_bytes=len(await file.read()),
    )
    return {"message": "File uploaded", "file": metadata}
