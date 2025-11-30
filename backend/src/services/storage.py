from pathlib import Path

from fastapi import UploadFile

from src.config import settings


class LocalStorageService:
    """Store files on local disk.

    This is a thin abstraction that will later be swapped for S3.
    """

    def __init__(self) -> None:
        self.base_dir = Path(settings.LOCAL_UPLOAD_DIR).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, upload: UploadFile) -> Path:
        target_path = self.base_dir / upload.filename
        # Stream to disk in chunks to avoid loading whole file in memory.
        with target_path.open("wb") as out:
            while True:
                chunk = await upload.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        await upload.close()
        return target_path
