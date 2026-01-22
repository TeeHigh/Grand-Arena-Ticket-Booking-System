from app.db.session import SessionLocal
from app.models.seat import Seat

db = SessionLocal()

seat = Seat(
    row="A",
    number=1,
    is_reserved=False
)

db.add(seat)
db.commit()
db.refresh(seat)

print(seat.id)

db.close()
