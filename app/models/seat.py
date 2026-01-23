from sqlalchemy import Column, Enum, Integer, String, DateTime
from app.db.base import Base
from app.models.enums import SeatStatus

class Seat(Base):
  __tablename__ = "seats"

  id = Column(Integer, primary_key=True, index=True)
  status = Column(
    Enum(SeatStatus, native_enum=True), 
      default=SeatStatus.AVAILABLE, 
      nullable=False
  )
  reserved_at = Column(DateTime(timezone=True), nullable=True)
  reservation_expires_at = Column(DateTime(timezone=True), nullable=True)
  reserved_by_user_id = Column(String, nullable=True)
