from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.seat import Seat
from app.models.enums import SeatStatus
from sqlalchemy import update, and_
from datetime import datetime, timezone


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


@staticmethod
def bulk_release_expired(db: Session) -> int:
    now = datetime.now(timezone.utc)
    
    stmt = (
        update(Seat)
        .where(
            and_(
                Seat.status == SeatStatus.RESERVED,
                Seat.reservation_expires_at < now
            )
        )
        .values(
            status=SeatStatus.AVAILABLE,
            reserved_by_user_id=None,
            reserved_at=None,
            reservation_expires_at=None
        )
        .execution_options(synchronize_session="fetch")
    )
    
    result = db.execute(stmt)
    db.commit()
    return result.rowcount