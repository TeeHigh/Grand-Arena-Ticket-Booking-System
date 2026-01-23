from sqlalchemy import func, text
from sqlalchemy.orm import Session
from app.models import seat
from app.models.seat import Seat
from app.models.enums import SeatStatus
from datetime import datetime, timezone


class SeatService:
    @staticmethod
    def _reset_if_expired(seat: Seat, db: Session) -> None:
      now = datetime.now(timezone.utc)

      try:
          if (
            seat.status == SeatStatus.RESERVED
            and seat.reservation_expires_at is not None
            and seat.reservation_expires_at < now
          ):
            seat.status = SeatStatus.AVAILABLE
            seat.reserved_at = None
            seat.reservation_expires_at = None
            seat.reserved_by_user_id = None

            db.flush()
      except:
          raise ValueError("Something went wrong")


    @staticmethod
    def reserve(seat_id: int, user_id: str, db: Session) -> Seat:
        """
        Reserve a seat for 5 minutes.
        Enforces:
        - row locking
        - expiration
        - idempotency
        """
        seat = (
            db.query(Seat)
            .filter(Seat.id == seat_id)
            .with_for_update()
            .first()
        )

        if not seat:
            raise ValueError("Seat not found")

        SeatService._reset_if_expired(seat, db)

        if seat.status == SeatStatus.RESERVED:
            if seat.reserved_by_user_id == user_id:
                return seat  # idempotent success
            raise ValueError("Seat already reserved")

        if seat.status == SeatStatus.CONFIRMED:
            raise ValueError("Seat already sold")

        seat.status = SeatStatus.RESERVED
        seat.reserved_at = func.now()
        seat.reservation_expires_at = func.now() + text("INTERVAL '5 minutes'")
        seat.reserved_by_user_id = user_id

        db.commit()
        db.refresh(seat)
        return seat

    @staticmethod
    def confirm(seat_id: int, user_id: str, db: Session) -> Seat:
        """
        Confirm a previously reserved seat.
        """
        seat = (
            db.query(Seat)
            .filter(Seat.id == seat_id)
            .with_for_update()
            .first()
        )

        if not seat:
            raise ValueError("Seat not found")

        SeatService._reset_if_expired(seat, db)

        if seat.status != SeatStatus.RESERVED and seat.status != SeatStatus.CONFIRMED:
            raise ValueError("Seat is not reserved")

        if seat.reserved_by_user_id != user_id:
            raise ValueError("Seat is reserved by another user")

        seat.status = SeatStatus.CONFIRMED

        db.commit()
        db.refresh(seat)
        return seat
