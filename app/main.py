import logging
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db
from .core.exceptions import AppException
from .dependencies.auth import get_current_user
from .models import User
from .routers import habit_cycles, habits

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Can declare global dependencies that will be combined with deps for each API Router
app = FastAPI(
    title="Habit Tracker API"
)

app.include_router(habit_cycles.router)
app.include_router(habits.router)

@app.exception_handler(AppException)
async def app_exception_handler(req: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message
            }
        }
    )

@app.get("/")
def read():
    logger.info("Testing logs")
    return {"message": "Hello"}

@app.get("/health", tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected"
            }
        )
    
