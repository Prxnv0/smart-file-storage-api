from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class FileMetadata:
    id: int
    filename: str
    content_type: str
    storage_path: str
    created_at: datetime


class FileMetadataService:
    """Simple in-memory metadata service.

    In production this will be replaced with a Postgres-backed repository.
    """

    def __init__(self) -> None:
        self._items: Dict[int, FileMetadata] = {}
        self._counter: int = 0

    def add_file(self, filename: str, content_type: str, storage_path: str) -> dict:
        self._counter += 1
        item = FileMetadata(
            id=self._counter,
            filename=filename,
            content_type=content_type,
            storage_path=storage_path,
            created_at=datetime.now(timezone.utc),
        )
        self._items[item.id] = item
        return asdict(item)

    def list_files(self) -> List[dict]:
        return [asdict(v) for v in self._items.values()]
