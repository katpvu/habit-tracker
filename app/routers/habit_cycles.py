from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.services.habit_service import HabitService
from ..schemas.habit import CycleResponse, CycleCreate
from ..models import User

router = APIRouter(
  prefix="/cycles",
  tags=["cycles"],
  dependencies=[]
)

@router.post("/{cycle_id}/activate", response_model=CycleResponse)
def activate_cycle(
  cycle_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """Activate a habit cycle by moving status from draft to active"""
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
  current_user: User = Depends(get_current_user)
):
  """Abandon active habit cycle"""
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
  current_user: User = Depends(get_current_user)
):
  """Create a new habit cycle in DRAFT status"""
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
  current_user: User = Depends(get_current_user)
):
  """Delete a DRAFT cycle"""
  habit_service = HabitService(db)
  habit_service.delete_cycle(
    user_id=current_user.id,
    cycle_id=cycle_id
  )
  return


# @router.patch("/{cycle_id}", response_model=CycleResponse)
# def update_cycle(
#   cycle_id: int,
#   updated_cycle: CycleUpdate,
#   db: Session = Depends(get_db),
#   current_user: User = Depends(get_current_user)
# ):
#   habit_service = HabitService(db)
#   cycle = habit_service.