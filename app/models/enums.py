import enum

class SeatStatus(str, enum.Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    CONFIRMED = "Confirmed"