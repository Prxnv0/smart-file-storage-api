from __future__ import annotations

from pathlib import PurePosixPath
from typing import Optional

import boto3
from fastapi import UploadFile

from src.config import settings


class S3StorageService:
    """Store files in an S3 bucket.

    This service uploads the incoming file stream directly to S3.
    """

    def __init__(self) -> None:
        if not settings.S3_BUCKET_NAME:
            raise ValueError("S3_BUCKET_NAME must be set when using S3 storage backend")

        self.bucket = settings.S3_BUCKET_NAME
        self.region = settings.AWS_REGION
        self.prefix = settings.S3_PREFIX or "uploads/"
        if not self.prefix.endswith("/"):
            self.prefix += "/"

        self._client = boto3.client("s3", region_name=self.region)

    async def save_file(self, upload: UploadFile) -> str:
        # Construct S3 key under the configured prefix
        key = str(PurePosixPath(self.prefix) / upload.filename)

        # Stream the uploaded file into S3
        # For simplicity we read it all at once; can be optimized to chunks later.
        body = await upload.read()
        await upload.close()

        self._client.put_object(Bucket=self.bucket, Key=key, Body=body, ContentType=upload.content_type)
        return key
