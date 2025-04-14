from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.location_review import LocationReview
from app.schemas.location_review import LocationReviewCreate, LocationReviewResponse
from app.auth.deps import get_current_user
from app.models.user import User
import uuid

router = APIRouter()

@router.get("/", response_model=List[LocationReviewResponse])
def list_location_reviews(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    reviews = db.query(LocationReview).offset(skip).limit(limit).all()
    return reviews

@router.get("/{review_id}", response_model=LocationReviewResponse)
def get_location_review(
    review_id: str,
    db: Session = Depends(get_db)
):
    review = db.query(LocationReview).filter(LocationReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/", response_model=LocationReviewResponse)
def create_location_review(
    review: LocationReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if reply_to_id exists if provided
    if review.reply_to_id:
        parent_review = db.query(LocationReview).filter(LocationReview.id == review.reply_to_id).first()
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
    db.commit()
    db.refresh(db_review)
    return db_review 