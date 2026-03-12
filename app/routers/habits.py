from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_discord_user
from app.models.user import User
from app.services.habit_service import HabitService
from ..schemas.habit import HabitAdd, HabitResponse, HabitUpdate, EntryResponse

router = APIRouter(
    prefix="/habits",
    tags=["habits"],
    dependencies=[]
)


@router.get("/{habit_id}/entries/today", response_model=Optional[EntryResponse])
def get_today_entry(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """
    Check if habit has an entry for today.
    Returns the entry if it exists, null otherwise.
    Used by Discord bot to check completion status.
    """
    habit_service = HabitService(db)
    entry = habit_service.get_entry_for_date(
        user_id=current_user.id,
        habit_id=habit_id,
        entry_date=date.today()
    )
    return entry


@router.post("", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def add_habit(
    new_habit: HabitAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Add a habit to a cycle. Habits can only be added to draft cycles."""
    habit_service = HabitService(db)
    habit = habit_service.add_habit_to_cycle(
        user_id=current_user.id,
        cycle_id=new_habit.habit_cycle_id,
        **new_habit.model_dump(exclude={'habit_cycle_id'})
    )
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Remove a habit from a cycle. Habits can only be removed from draft cycles."""
    habit_service = HabitService(db)
    habit_service.remove_habit_from_cycle(
        user_id=current_user.id,
        habit_id=habit_id
    )
    return


@router.patch("/{habit_id}", response_model=HabitResponse, status_code=status.HTTP_200_OK)
def update_habit(
    habit_id: int,
    updates: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Update habit in a cycle. Habits can only be updated in a draft cycle."""
    habit_service = HabitService(db)
    habit = habit_service.update_habit(
        user_id=current_user.id,
        habit_id=habit_id,
        updates=updates
    )
    return habit


@router.post("/{habit_id}/complete", response_model=EntryResponse)
def log_habit_complete(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_discord_user)
):
    """Mark a habit as complete for today."""
    habit_service = HabitService(db)
    entry = habit_service.add_entry(
        user_id=current_user.id,
        habit_id=habit_id,
        completed=True
    )
    return entry
