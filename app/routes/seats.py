from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.enums import SeatStatus
from app.models.seat import Seat
from app.services.seat_service import SeatService

router = APIRouter(prefix="/seats", tags=["Seats"])

@router.get("/")
def list_seats(db: Session = Depends(get_db)):
  seats = db.query(Seat).all()
  return seats

@router.post("/{seat_id}/reserve")
def reserve_seat(
    seat_id: int,
    user_id: str,
    db: Session = Depends(get_db),
):
    try:
        seat = SeatService.reserve(seat_id, user_id, db)
        return {"message": "Seat reserved successfully", "seat_id": seat.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{seat_id}/confirm")
def confirm_seat(
    seat_id: int,
    user_id: str,
    db: Session = Depends(get_db),
):
    try:
        seat = SeatService.confirm(seat_id, user_id, db)
        return {"message": "Seat confirmed successfully", "seat_id": seat.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))