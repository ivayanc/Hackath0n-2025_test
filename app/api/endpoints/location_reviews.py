from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.models.location_review import LocationReview
from app.schemas.location_review import LocationReviewCreate, LocationReviewResponse
from app.auth.auth0 import get_current_user
from app.models.user import User
import uuid

router = APIRouter()

@router.get("/for_location/{location_id}", response_model=List[LocationReviewResponse])
async def list_location_reviews(
    location_id: str,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    stmt = select(LocationReview).where(LocationReview.location_id == location_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    reviews = result.scalars().all()
    return reviews

@router.get("/{review_id}", response_model=LocationReviewResponse)
async def get_location_review(
    review_id: str,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(LocationReview).where(LocationReview.id == review_id)
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/", response_model=LocationReviewResponse)
async def create_location_review(
    review: LocationReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if reply_to_id exists if provided
    if review.reply_to_id:
        stmt = select(LocationReview).where(LocationReview.id == review.reply_to_id)
        result = await db.execute(stmt)
        parent_review = result.scalar_one_or_none()
        if not parent_review:
            raise HTTPException(status_code=404, detail="Parent review not found")

    db_review = LocationReview(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        location_id=review.location_id,
        rating=review.rating,
        review=review.review,
        reply_to_id=review.reply_to_id
    )
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review 