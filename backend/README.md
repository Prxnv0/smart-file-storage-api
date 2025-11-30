# Smart File Storage & Processing System (Backend)

Backend-only FastAPI application for uploading files, storing them (local for now), and managing file metadata. Designed to be cloud-native and ready for AWS (S3, RDS, Lambda, ECS Fargate, ECR, GitHub Actions).

---

## Project Structure

```bash
backend/
  app.py                # Uvicorn entrypoint (FastAPI app instance)
  requirements.txt      # Python dependencies
  Dockerfile            # Container image for FastAPI app
  docker-compose.yml    # Local development composition
  .env.example          # Example environment variables
  src/
    main.py             # FastAPI application factory
    config.py           # Settings via environment variables
    routes/
      __init__.py
      health.py         # /health endpoint
      files.py          # /files and /files/upload endpoints
    services/
      __init__.py
      metadata.py       # In-memory metadata store (Postgres later)
      storage.py        # Local file storage (S3 later)
    utils/
      __init__.py
  data/
    uploads/            # Local upload directory (created at runtime)
```

---

## Configuration

The app uses environment variables (via `pydantic.BaseSettings`). See `.env.example`.

Copy the example file and adjust values as needed:

```bash
cp .env.example .env
```

Key variables:

- `APP_ENV` – environment name (`local`, `docker-local`, `prod`, ...)
- `LOCAL_UPLOAD_DIR` – directory for local file storage
- `AWS_REGION`, `S3_BUCKET_NAME` – placeholders for future S3 integration
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` – placeholders for Postgres (RDS later)

---

## Running Locally (without Docker)

Prerequisites: Python 3.10+, pip, virtualenv recommended.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# (optional) create .env from example
cp .env.example .env

# Run FastAPI app
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`.

---

## Running via Docker

Build and run with Docker Compose:

```bash
cd backend
docker compose up --build
```

This will:

- Build the `api` image from the `Dockerfile`
- Run the container exposing `http://localhost:8000`
- Mount `./data/uploads` to `/data/uploads` in the container

To stop:

```bash
docker compose down
```

---

## API Endpoints

### Health Check

- **Method**: `GET /health`
- **Description**: Simple health/uptime check.

Example with `curl`:

```bash
curl http://localhost:8000/health
```

---

### List Files

- **Method**: `GET /files`
- **Description**: Returns a list of file metadata stored in the in-memory store.

Example:

```bash
curl http://localhost:8000/files
```

Response (example):

```json
[
  {
    "id": 1,
    "filename": "example.png",
    "content_type": "image/png",
    "storage_path": "./data/uploads/example.png",
    "created_at": "2025-01-01T12:00:00+00:00"
  }
]
```

> Note: Metadata is in-memory only for now, so it resets when the app restarts. This will later be backed by Postgres.

---

### Upload File

- **Method**: `POST /files/upload`
- **Description**: Upload a file. The file is stored on local disk and metadata is stored in-memory.
- **Body**: `multipart/form-data` with a single field `file`.

Example with `curl`:

```bash
curl -X POST "http://localhost:8000/files/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/file.txt"
```

Example response:

```json
{
  "message": "File uploaded",
  "file": {
    "id": 1,
    "filename": "file.txt",
    "content_type": "text/plain",
    "storage_path": "./data/uploads/file.txt",
    "created_at": "2025-01-01T12:00:00+00:00"
  }
}
```

---

## Ready for AWS Integration

This starter is structured for later integration with:

- **S3**: replace `LocalStorageService` with an S3-backed implementation
- **RDS Postgres**: replace `FileMetadataService` with a DB repository
- **Lambda**: configure S3 event notifications to trigger a Lambda function on file upload
- **ECS Fargate + ECR**: use this `Dockerfile` to build an image, push to ECR, and deploy on ECS Fargate behind an ALB
- **GitHub Actions**: CI/CD pipeline can run tests, build/push the image, and update ECS tasks

No authentication is added yet (prototype phase). All endpoints are open.
