from typing import List, Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from app.core.config import settings
from app.core.exceptions import NotFoundError, ValidationError, ConflictError
from ..models import HabitEntry, Habit, HabitCycle, CycleStatuses, CycleTypes
from app.schemas.habit import HabitUpdate
from datetime import date

"""
Habit service layer that contains all the business logic pertaining to habit cycle management, CRUD operations for habits, and habit entries
"""
class HabitService:
  def __init__(self, db: Session):
    self.db = db

  # ============== CYCLE MANAGEMENT ================
  def create_cycle(self, user_id: int, name: str, cycle_type: CycleTypes) -> HabitCycle:
    # Check if user already has an active cycle of that type
    existing_active_cycle = self.db.query(HabitCycle).filter(
      HabitCycle.user_id == user_id,
      HabitCycle.cycle_type == cycle_type,
      HabitCycle.status == CycleStatuses.ACTIVE
    ).first()

    if existing_active_cycle:
      raise ConflictError(f"Active {cycle_type.value} cycle already exists")

    # Create new habit cycle
    new_cycle = HabitCycle(
      user_id=user_id,
      cycle_type=cycle_type,
      name=name
    )

    # Add to DB
    self.db.add(new_cycle)
    self.db.commit()
    self.db.refresh(new_cycle)

    return new_cycle

  def get_cycles_for_user(self, user_id: int, statuses: Optional[List[CycleStatuses]] = None) -> List[HabitCycle]:
    filters = [ HabitCycle.user_id == user_id ]

    if statuses is not None:
      filters.append(HabitCycle.status.in_(statuses))
    
    cycles = self.db.query(HabitCycle).filter(*filters).all()

    return cycles

  def activate_cycle(self, user_id: int, cycle_id: int) -> HabitCycle:
    min_habits_required_to_start_cycle = settings.MIN_HABITS_REQUIRED_TO_START_CYCLE

    cycle = self._get_cycle(cycle_id, user_id)

    # Can only activate draft cycles
    if cycle.status != CycleStatuses.DRAFT:
      raise ValidationError("Can only activate cycles in DRAFT status")

    if len(cycle.habits) < min_habits_required_to_start_cycle:
      raise ValidationError(f"Cycle needs at least {min_habits_required_to_start_cycle} habits to activate")

    existing_active_cycle = self.db.query(HabitCycle).filter(
      HabitCycle.user_id == user_id,
      HabitCycle.cycle_type == cycle.cycle_type,
      HabitCycle.status == CycleStatuses.ACTIVE
    ).first()

    if existing_active_cycle is not None:
      raise ConflictError(f"Active {cycle.cycle_type.value} cycle already exists")
    
    # If all those above checks pass, then update the cycle status to active, and set started_at
    cycle.status = CycleStatuses.ACTIVE
    cycle.started_at = datetime.now(timezone.utc)

    self.db.commit()
    return cycle

  def delete_cycle(self, user_id: int, cycle_id: int) -> None:
    cycle = self._get_cycle(cycle_id, user_id)
    
    if cycle.status != CycleStatuses.DRAFT:
      raise ValidationError(f"Cannot delete cycle with '{cycle.status.value}' status. Only DRAFT cycles can be deleted.")
    
    self.db.delete(cycle)
    self.db.commit()

  def abandon_cycle(self, user_id: int, cycle_id: int) -> HabitCycle:
    cycle = self._get_cycle(cycle_id, user_id)
    
    if cycle.status == CycleStatuses.ABANDONED:
      raise ValidationError("Cycle already abandoned")

    if cycle.status in [CycleStatuses.DRAFT, CycleStatuses.COMPLETED]:
      raise ValidationError(f"{cycle.status.value} cycles cannot be abandoned")
    
    cycle.status = CycleStatuses.ABANDONED

    self.db.commit()
    self.db.refresh(cycle)

    return cycle
  
  def complete_cycle(self, user_id: int, cycle_id: int) -> HabitCycle:
    cycle = self._get_cycle(cycle_id, user_id)

    if cycle.status == CycleStatuses.COMPLETED:
      return cycle

    if cycle.status != CycleStatuses.ACTIVE:
      raise ValidationError(f"Cannot mark {cycle.status.value} cycles as complete. Cycle must be of ACTIVE status")

    cycle.status = CycleStatuses.COMPLETED
    cycle.completed_at = datetime.now(timezone.utc)

    self.db.commit()
    self.db.refresh(cycle)

    return cycle
  
  def get_habits_from_cycle(self, user_id: int, cycle_id: int ) -> List[Habit]:
    cycle = self._get_cycle(cycle_id, user_id)
    return cycle.habits 
  
  # ============== HABIT MANAGEMENT ================

  # Add a new habit to a draft habit cycle
  def add_habit_to_cycle(self, user_id: int, cycle_id: int, name: str) -> Habit:
    cycle = self._get_cycle(cycle_id, user_id)
    self._validate_cycle_is_draft(cycle)

    new_habit = Habit(
      habit_cycle_id=cycle_id,
      name=name
    )

    self.db.add(new_habit)

    try:
      self.db.commit()
    except IntegrityError:
      self.db.rollback()
      raise ConflictError(f"Habit '{name}' already exists in this cycle")
      
    self.db.refresh(new_habit)

    return new_habit

  # Remove a habit from a draft habit cycle
  def remove_habit_from_cycle(self, user_id: int, habit_id: int) -> None:
    habit = self._get_habit(user_id, habit_id)
    self._validate_cycle_is_draft(habit.habit_cycle)

    self.db.delete(habit)
    self.db.commit()

  # Update a habit from a draft habit cycle
  def update_habit(self, user_id: int, habit_id: int, updates: HabitUpdate) -> Habit:
    habit = self._get_habit(user_id, habit_id)
    self._validate_cycle_is_draft(habit.habit_cycle)

    # Only get fields that were actually set in the request
    update_data = updates.model_dump(exclude_unset=True)

    # Apply each update
    for field, value in update_data.items():
      setattr(habit, field, value)

    try:
      self.db.commit()
    except IntegrityError:
      self.db.rollback()
      raise ConflictError(f"Habit '{updates.name}' already exists in this cycle")
    
    self.db.refresh(habit)
    return habit 

  # ============== ENTRY MANAGEMENT ================

  def get_entry_for_date(self, user_id: int, habit_id: int, entry_date: date) -> Optional[HabitEntry]:
    """
    Get habit entry for a specific date.
    Returns None if no entry exists for that date.
    Validates habit ownership via _get_habit().
    """
    # Verify habit belongs to user (raises NotFoundError if not)
    habit = self._get_habit(user_id, habit_id)

    # Query for entry on specific date
    entry = self.db.query(HabitEntry).filter(
        HabitEntry.habit_id == habit.id,
        HabitEntry.entry_date == entry_date
    ).first()

    return entry

  # Add a habit entry
  def add_entry(self, user_id: int, habit_id: int, completed: bool) -> HabitEntry:
    habit = self._get_habit(
      user_id=user_id, 
      habit_id=habit_id
    )

    cycle = habit.habit_cycle

    if cycle.status is not CycleStatuses.ACTIVE:
      raise ValidationError(f"Cannot add entry for a cycle that is not active")
    
    habit_entry = HabitEntry(
      habit_id=habit_id,
      entry_date=date.today()
    )

    if completed:
      habit_entry.mark_complete()

    try:
      self.db.add(habit_entry)
      self.db.commit()
    except IntegrityError:
      # DB constraint on habit_id and entry_date to prevent duplicate entries 
      self.db.rollback()
      raise ConflictError("Entry for this habit already exists")
      

    self.db.refresh(habit_entry)
    return habit_entry
  
  # Private methods
  def _get_cycle(self, cycle_id: int, user_id: int) -> HabitCycle:
    cycle = self.db.query(HabitCycle).filter(
      HabitCycle.id == cycle_id,
      HabitCycle.user_id == user_id
    ).first()

    if cycle is None:
      raise NotFoundError("Cycle", str(cycle_id))
    
    return cycle

  def _get_habit(self, user_id: int, habit_id: int) -> Habit:
    habit = self.db.query(Habit).join(HabitCycle).filter(
      Habit.id == habit_id,
      HabitCycle.user_id == user_id
    ).first()

    if habit is None:
      raise NotFoundError("Habit", habit_id)

    return habit
  
  def _validate_cycle_is_draft(self, cycle: HabitCycle) -> None:
    if cycle.status != CycleStatuses.DRAFT:
      raise ValidationError(
        f"Cannot modify cycle with '{cycle.status.value}' status. Only DRAFT cycles can be modified."
      )
