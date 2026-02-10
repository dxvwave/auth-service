import logging
from fastapi import APIRouter, Depends

from core.dependencies import get_current_active_user
from core.schemas.user import UserResponse
from db.models import User

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_active_user),
):
    return UserResponse(**current_user.__dict__)
