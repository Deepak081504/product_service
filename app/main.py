import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers.product_controller import router as product_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("REST Product Service started successfully")

    yield

    logger.info("REST Product Service shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    description="REST API for Product Management",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)


@app.get("/health", tags=["Health"])
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


app.include_router(product_router)
