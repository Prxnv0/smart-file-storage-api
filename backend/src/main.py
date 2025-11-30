from fastapi import FastAPI

from src.config import settings
from src.routes.health import router as health_router
from src.routes.files import router as files_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # Register API routers
    app.include_router(health_router)
    app.include_router(files_router)

    return app
