# Smart File Storage & Processing System

Cloud‑native file storage backend with S3 + RDS, and a simple React frontend for uploads and browsing metadata.

## High‑Level Architecture

- **Frontend**: React + Vite + TypeScript  
  Upload files and show list of uploaded files.
- **Backend**: FastAPI (Python)  
  Stores files in **Amazon S3** and metadata in **PostgreSQL** (RDS in prod, Docker Postgres in local dev).
- **Infrastructure**: Docker + Docker Compose (local & EC2), AWS S3, AWS RDS Postgres, EC2, ECR, GitHub Actions.

## Repository Structure

```text
.
├── backend/
│   ├── app.py                  # Uvicorn entrypoint (app = create_app())
│   ├── Dockerfile              # Backend container image
│   ├── docker-compose.yml      # API + Postgres (for local/dev or EC2-with-local-DB)
│   ├── requirements.txt
│   ├── .env                    # Backend env vars (NOT committed in prod)
│   └── src/
│       ├── __init__.py
│       ├── main.py             # create_app(): CORS, DB init, router registration
│       ├── config.py           # Pydantic Settings (env-based config)
│       ├── db.py               # SQLAlchemy engine + Session + get_db()
│       ├── models.py           # FileRecord model
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── health.py       # /health
│       │   └── files.py        # /files, /files/upload
│       └── services/
│           ├── __init__.py
│           ├── storage.py      # Local storage (dev)
│           ├── storage_s3.py   # S3 storage implementation
│           └── metadata_db.py  # DB-backed metadata service
│
├── smart-file-storage-frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── .env                    # VITE_API_BASE_URL=...
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/
│       │   └── client.ts       # uploadFile, listFiles
│       └── components/
│           ├── FileUploadForm.tsx
│           └── FileList.tsx
│
└── .github/
    └── workflows/
        └── ci-cd.yml           # Build & push backend image to ECR
```

## Backend Overview

- FastAPI app with endpoints:
  - `GET /health` – health check.
  - `POST /files/upload` – multipart upload (`file` field), stores file in S3 and metadata in Postgres.
  - `GET /files` – returns list of stored file metadata from Postgres.
- Configuration via `backend/.env` and `src/config.py`.
- CORS enabled globally in `src/main.py` using `CORSMiddleware`.
- SQLAlchemy models and DB session helper in `src/models.py` and `src/db.py`.
- Metadata persisted to Postgres (local Docker Postgres or AWS RDS Postgres).

### Running Backend Locally (without Docker)

```bash
cd backend

# 1) Create & activate virtualenv (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Create .env (based on .env.example)

# 4) Run FastAPI
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI: `http://localhost:8000/docs`

### Running Backend with Docker (Local)

```bash
cd backend

# Start API + Postgres
docker-compose up --build

# or detached
docker-compose up --build -d

# View logs
docker-compose logs -f
```

API: `http://localhost:8000`  
Postgres: `localhost:5432` (mapped from container)

## EC2 Deployment (Docker Compose)

1. **Provision EC2**
   - Amazon Linux, Docker + docker-compose installed.
   - Attach IAM Role with permissions for S3 and RDS.

2. **Clone repo on EC2**

```bash
git clone <your-repo-url> smart-file-storage-api
cd smart-file-storage-api/backend
cp .env.example .env          # then edit for RDS + S3
```

3. **Configure `.env` for RDS + S3**

```env
DB_HOST=<your-rds-endpoint>
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=********

STORAGE_BACKEND=s3
AWS_REGION=eu-north-1
S3_BUCKET_NAME=smart-file-storage-psingh-uploads
S3_PREFIX=uploads/
```

4. **Start services**

```bash
cd backend
docker-compose up --build -d
docker-compose ps
```

5. Access API at `http://<EC2_PUBLIC_IP>:8000/docs` from your browser.

To deploy new versions manually:

```bash
# On laptop
git commit -am "..."
git push

# On EC2
cd /home/ec2-user/smart-file-storage-api
git pull
cd backend
docker-compose up --build -d
```

## Frontend Overview

- React + Vite + TypeScript app in `smart-file-storage-frontend/`.
- Two main components:
  - `FileUploadForm` – uploads file via `POST /files/upload`.
  - `FileList` – loads metadata via `GET /files` and shows a table.
- API calls wrapped in `src/api/client.ts`.

### Frontend Environment

`smart-file-storage-frontend/.env`:

```env
VITE_API_BASE_URL=http://<EC2_PUBLIC_IP>:8000
```

For local backend, use `http://localhost:8000`.

### Running Frontend (Dev)

```bash
cd smart-file-storage-frontend
npm install
npm run dev
```

Dev URL: `http://localhost:5173`

## CI/CD (Backend → ECR)

GitHub Actions workflow: `.github/workflows/ci-cd.yml`.

On push to the configured branch it:

1. Checks out the repository.
2. Configures AWS credentials using OIDC.
3. Logs in to Amazon ECR.
4. Builds and pushes the backend Docker image tagged as `${ECR_REPOSITORY}:${IMAGE_TAG}`.

A deploy step to ECS Fargate or EC2 can be added later using `aws ecs update-service` or SSM/SSH.

## Future Work

- Add ECS Fargate deployment using the ECR image.
- Add Lambda processing on S3 `ObjectCreated` events.
- Lock down CORS to the actual frontend origin.
- Add authentication/authorization and rate limiting.
