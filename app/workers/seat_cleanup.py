from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.seat import Seat
from app.models.enums import SeatStatus


def cleanup_expired_seats():
    """
    Frees seats whose reservation has expired.
    Runs periodically in the background.
    """
    db: Session = SessionLocal()

    try:
        expired_seats = (
            db.query(Seat)
            .filter(
                Seat.status == SeatStatus.RESERVED,
                Seat.reservation_expires_at < func.now()
            )
            .all()
        )

        for seat in expired_seats:
            seat.status = SeatStatus.AVAILABLE
            seat.reserved_at = None
            seat.reservation_expires_at = None
            seat.reserved_by_user_id = None

        if expired_seats:
            db.commit()

    finally:
        db.close()
