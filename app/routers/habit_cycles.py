import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_discord_user
from app.services.habit_service import HabitService
from ..schemas.habit import CycleResponse, CycleCreate, CycleListResponse
from ..models import User, CycleStatuses

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/cycles",
    tags=["cycles"],
    dependencies=[]
)


@router.get("", response_model=List[CycleListResponse])
def list_cycles(
    status: Optional[str] = Query(None, description="Filter by status: draft, active, completed, abandoned"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """List user's habit cycles, optionally filtered by status."""
    habit_service = HabitService(db)

    # Convert status string to CycleStatuses enum if provided
    status_filter = None
    if status:
        try:
            status_enum = CycleStatuses(status.lower())
            status_filter = [status_enum]
        except ValueError:
            pass  # Invalid status - return all cycles

    cycles = habit_service.get_cycles_for_user(
        user_id=current_user.id,
        statuses=status_filter
    )

    return cycles


@router.get("/{cycle_id}", response_model=CycleResponse)
def get_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Get a specific cycle with all its habits."""
    habit_service = HabitService(db)
    cycle = habit_service._get_cycle(cycle_id, current_user.id)
    return cycle


@router.post("/{cycle_id}/activate", response_model=CycleResponse)
def activate_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Activate a habit cycle by moving status from draft to active."""
    habit_service = HabitService(db)
    cycle = habit_service.activate_cycle(
        user_id=current_user.id,
        cycle_id=cycle_id
    )
    return cycle


@router.post("/{cycle_id}/abandon", response_model=CycleResponse)
def abandon_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Abandon active habit cycle."""
    habit_service = HabitService(db)
    cycle = habit_service.abandon_cycle(
        user_id=current_user.id,
        cycle_id=cycle_id
    )
    return cycle


@router.post("", response_model=CycleResponse, status_code=status.HTTP_201_CREATED)
def create_cycle(
    new_cycle: CycleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Create a new habit cycle in DRAFT status."""
    logger.info(f"Creating cycle for user {current_user.id}", extra={"user_id": current_user.id})
    habit_service = HabitService(db)
    cycle = habit_service.create_cycle(
        user_id=current_user.id,
        **new_cycle.model_dump()
    )
    return cycle


@router.delete("/{cycle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_draft_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Delete a DRAFT cycle."""
    habit_service = HabitService(db)
    habit_service.delete_cycle(
        user_id=current_user.id,
        cycle_id=cycle_id
    )
    return