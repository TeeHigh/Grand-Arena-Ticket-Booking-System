from app.db.session import SessionLocal
from app.models.seat import Seat
from app.models.enums import SeatStatus

def seed_arena():
    db = SessionLocal()
    try:
        # Check if seats already exist to prevent duplicate seeding
        count = db.query(Seat).count()
        if count > 0:
            print(f"Arena already seeded with {count} seats. Skipping.")
            return

        print("Initializing 100 VIP Seats for the Grand Arena...")
        seats = []
        for num in range(1, 101):
            seats.append(Seat(
                id=num,
                status=SeatStatus.AVAILABLE
            ))
        
        db.add_all(seats)
        db.commit()
        print("Success: Grand Arena is ready for bookings!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_arena()