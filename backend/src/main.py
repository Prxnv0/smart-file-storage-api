from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routes.health import router as health_router
from src.routes.files import router as files_router
from src.db import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # CORS: allow all origins for now (suitable for development).
    # In production, restrict allowed_origins to your frontend domains.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create database tables (simple auto-migration for now)
    Base.metadata.create_all(bind=engine)

    # Register API routers
    app.include_router(health_router)
    app.include_router(files_router)

    return app
