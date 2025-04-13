from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.models.location import LocationType

class Coordinates(BaseModel):
    lat: float
    lng: float

class LocationBase(BaseModel):
    name: str
    coordinates: Coordinates
    factors: Optional[Dict[str, Any]] = None
    type: LocationType
    description: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: str

    class Config:
        from_attributes = True 