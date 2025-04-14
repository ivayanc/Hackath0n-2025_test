from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.user import UserResponse

class LocationReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review: str
    reply_to_id: Optional[str] = None

class LocationReviewCreate(LocationReviewBase):
    location_id: str

class LocationReviewResponse(LocationReviewBase):
    id: str
    user: UserResponse
    location_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
