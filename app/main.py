from fastapi import FastAPI
from app.routes import seats
from apscheduler.schedulers.background import BackgroundScheduler
from app.workers.seat_cleanup import cleanup_expired_seats
app = FastAPI(title="Grand Arena API")

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_expired_seats, "interval", minutes=1)
scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(seats.router)
