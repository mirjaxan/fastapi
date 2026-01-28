import logging

from fastapi import FastAPI 
from contextlib import asynccontextmanager

from .v1.users import user_router
from app.settings import settings
from app.services.logger import get_logger
from sqlalchemy import text
from app.db.session import SessionLocal
from ..services.pycache_cleaner import remove_pycaches_and_pycs
from ..settings import BASE_DIR

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
	
	try:
		with SessionLocal() as db:
			db.execute(text("SELECT 1"))
			logger.info("Database Connected")
	except Exception as e:
		logger.info(f"Databse connection error: {e}")
	remove_pycaches_and_pycs(BASE_DIR)
	yield

app = FastAPI(title="My project", version="1.0.0", lifespan=lifespan)

app.include_router(user_router, prefix="/api/v1/users")