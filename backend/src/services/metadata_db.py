from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from src.models import FileRecord


class DbFileMetadataService:
    """Persist file metadata in a relational database (Postgres)."""

    def __init__(self, db: Session):
        self.db = db

    def list_files(self) -> list[dict]:
        records = self.db.query(FileRecord).order_by(FileRecord.created_at.desc()).all()
        return [self._to_dict(r) for r in records]

    def create_file(
        self,
        *,
        filename: str,
        content_type: str,
        storage_path: str,
        size_bytes: int | None = None,
    ) -> dict:
        record = FileRecord(
            filename=filename,
            content_type=content_type,
            storage_path=storage_path,
            size_bytes=size_bytes,
            created_at=datetime.utcnow(),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return self._to_dict(record)

    @staticmethod
    def _to_dict(record: FileRecord) -> dict:
        return {
            "id": record.id,
            "filename": record.filename,
            "content_type": record.content_type,
            "storage_path": record.storage_path,
            "created_at": record.created_at.isoformat(),
        }
