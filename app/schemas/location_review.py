from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

class LocationReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review: str
    reply_to_id: Optional[str] = None

class LocationReviewCreate(LocationReviewBase):
    location_id: str

class LocationReviewResponse(LocationReviewBase):
    id: str
    user_id: str
    location_id: str
    created_at: datetime
    updated_at: datetime

    @field_validator('created_at', 'updated_at', mode='before')
    def parse_datetime(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid datetime format")
        return value

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.isoformat()}
    ) 