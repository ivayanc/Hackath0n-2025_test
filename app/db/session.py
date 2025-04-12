from typing import AsyncGenerator
from app.db.base import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator:
    session = AsyncSessionLocal()
    try:
        logger.debug("Creating new database session")
        yield session
    except Exception as e:
        logger.error(f"Error during database session: {e}")
        await session.rollback()
        raise
    finally:
        logger.debug("Closing database session")
        await session.close() 