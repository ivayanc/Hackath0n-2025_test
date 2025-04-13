from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.db.session import get_db
from app.schemas.location import Location, LocationCreate
from app.models.location import Location as LocationModel

router = APIRouter()

@router.post("/", response_model=Location)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = LocationModel(
        id=str(uuid.uuid4()),
        name=location.name,
        coordinates=location.coordinates.dict(),
        factors=location.factors,
        type=location.type,
        description=location.description
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.get("/", response_model=List[Location])
def list_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = db.query(LocationModel).offset(skip).limit(limit).all()
    return locations 