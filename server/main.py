from fastapi import FastAPI
from loguru import logger
import uvicorn

app = FastAPI(title="RealTimeCollab - Backend (FastAPI)")

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