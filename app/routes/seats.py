from fastapi import APIRouter

router = APIRouter(prefix="/seats", tags=["Seats"])

@router.get("/")
def list_seats():
  return []

