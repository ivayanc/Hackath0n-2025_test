from sqlalchemy import Column, String, Enum, JSON
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base_class import Base
import enum

class LocationType(str, enum.Enum):
    EDUCATION = "education"
    ENJOY = "enjoy"
    INTERESTING = "interesting"

class Location(Base):
    __tablename__ = "locations"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    coordinates = Column(JSON, nullable=False)  # Will store {lat: float, lng: float}
    factors = Column(JSONB, nullable=True)  # For storing flexible JSON data
    type = Column(Enum(LocationType), nullable=False)
    description = Column(String, nullable=True) 