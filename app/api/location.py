from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional
import uuid

from app.db.session import get_db
from app.schemas.location import Location, LocationCreate
from app.models.location import Location as LocationModel, LocationType

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
async def list_locations(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    types: Optional[List[LocationType]] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(LocationModel)
    
    # Apply search filter if provided
    if search:
        search_filter = or_(
            LocationModel.name.ilike(f"%{search}%"),
            LocationModel.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Apply type filter if provided
    if types:
        query = query.filter(LocationModel.type.in_(types))
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    locations = result.scalars().all()
    return locations 