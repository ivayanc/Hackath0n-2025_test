from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class LocationReview(Base):
    __tablename__ = "location_reviews"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    location_id = Column(String, ForeignKey("locations.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)
    reply_to_id = Column(String, ForeignKey("location_reviews.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="location_reviews")
    location = relationship("Location", back_populates="reviews")
    reply_to = relationship("LocationReview", remote_side=[id], backref="replies") 