import logging


from fastapi import APIRouter, Depends
from app.auth.auth0 import get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    logger.info(f"Getting information for user: {current_user.id}")
    return current_user
