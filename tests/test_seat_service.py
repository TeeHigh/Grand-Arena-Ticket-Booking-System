import app
from app.models.enums import SeatStatus
from app.models.seat import Seat
from tests.conftest import override_get_db
import asyncio
import pytest
from httpx import AsyncClient

def test_list_seats_empty(client):
    response = client.get("/seats/")
    assert response.status_code == 200
    assert response.json() == []

def test_reserve_seat_success(client):
    # First, create a seat directly in the test database
    db = next(override_get_db())
    new_seat = Seat(status=SeatStatus.AVAILABLE)
    db.add(new_seat)
    db.commit()
    db.refresh(new_seat)

    response = client.post(f"/seats/{new_seat.id}/reserve", params={"user_id": "user1"})
    assert response.status_code == 200
    assert response.json()["message"] == "Seat reserved successfully"
    assert response.json()["seat_id"] == new_seat.id


def test_reserve_seat_already_reserved(client):
    db = next(override_get_db())
    new_seat = Seat(status=SeatStatus.RESERVED, reserved_by_user_id="user2")
    db.add(new_seat)
    db.commit()
    db.refresh(new_seat)

    response = client.post(f"/seats/{new_seat.id}/reserve", params={"user_id": "user1"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Seat already reserved"


