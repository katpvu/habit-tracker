import logging
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
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
