from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.habit_service import HabitService
from ..schemas.habit import HabitAdd, HabitResponse, HabitUpdate

router = APIRouter(
  prefix="/habits",
  tags=["habits"],
  dependencies=[]
)

@router.post("", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def add_habit(
  new_habit: HabitAdd,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user) 
):
  """Add a habit to a cycle. Habits can only be added to draft cycles"""
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
  current_user: User = Depends(get_current_user)
):
  """Remove a habit from a cycle. Habits can only be removed from draft cycles"""
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
  current_user: User = Depends(get_current_user)
):
  """Update habit in a cycle. Habits can only be updated in a draft cycle"""
  habit_service = HabitService(db)
  habit = habit_service.update_habit(
    user_id=current_user.id,
    habit_id=habit_id,
    updates=updates
  )
  return habit