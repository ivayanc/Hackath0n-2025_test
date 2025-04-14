from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime

class LocationReview(Base):
    __tablename__ = "location_reviews"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    location_id = Column(String, ForeignKey("locations.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)
    reply_to_id = Column(String, ForeignKey("location_reviews.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="location_reviews")
    location = relationship("Location", back_populates="reviews")
    reply_to = relationship("LocationReview", remote_side=[id], backref="replies") 