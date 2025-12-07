from fastapi import FastAPI
from loguru import logger
import uvicorn
from api import users, auth

from app.core.database import init_db

app = FastAPI(title="RealTimeCollab - Backend (FastAPI)")
app.include_router(users.router)
app.include_router(auth.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database schema...")
    await init_db()
    logger.info("Database initialized successfully.")

@app.get("/ping")
async def ping():
    logger.info("Ping endpoint hit")
    return {"status": "ok", "message": "FastAPI is up!"}
if __name__ == "__main__":
   uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
   )