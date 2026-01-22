from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base

class Seat(Base):
  __tablename__ = "seats"

  id = Column(Integer, primary_key=True, index=True)
  status = Column(String, nullable=False)
  reserved_at = Column(DateTime(timezone=True), nullable=True)
  reservation_expires_at = Column(DateTime(timezone=True), nullable=True)
  reserved_by_user_id = Column(String, nullable=True)
