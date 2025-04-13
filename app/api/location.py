from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.db.session import get_db
from app.schemas.location import Location, LocationCreate
from app.models.location import Location as LocationModel

router = APIRouter()

@router.post("/", response_model=Location)
async def create_location(location: LocationCreate, db: AsyncSession = Depends(get_db)):
    db_location = LocationModel(
        id=str(uuid.uuid4()),
        name=location.name,
        coordinates=location.coordinates.dict(),
        factors=location.factors,
        type=location.type,
        description=location.description
    )
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location

@router.get("/", response_model=List[Location])
async def list_locations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(LocationModel).offset(skip).limit(limit)
    result = await db.execute(query)
    locations = result.scalars().all()
    return locations 