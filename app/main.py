from fastapi import FastAPI
from app.routes import seats

app = FastAPI(title="Grand Arena API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(seats.router)
