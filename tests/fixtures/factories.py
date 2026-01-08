from app.models import User, HabitCycle, Habit, CycleTypes, CycleStatuses, HabitEntry
from sqlalchemy.orm import Session
from datetime import datetime, date


class UserFactory:
  @staticmethod
  def create(db: Session, **kwargs) -> User:
    user = User(**kwargs)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
  
class CycleFactory:
  @staticmethod
  def create(db: Session, user_id: int, **kwargs) -> HabitCycle:
    """Creates cycle and save into DB"""
    defaults = {
      "name": "Test Cycle",
      "cycle_type": CycleTypes.DAILY,
      "status": CycleStatuses.DRAFT
    }
    defaults.update(kwargs)

    cycle = HabitCycle(
      user_id=user_id,
      **defaults
    )

    db.add(cycle)
    db.commit()
    db.refresh(cycle)
    return cycle
  
  @staticmethod
  def create_with_habits(db: Session, user_id: int, num_habits: int = 3) -> HabitCycle:
    """Create cycle with specified number of habits and save into DB"""
    cycle = CycleFactory.create(db, user_id)

    for i in range(num_habits):
      habit = Habit(
        habit_cycle_id=cycle.id,
        name=f"Habit {i+1}"
      )
      db.add(habit)
      
    db.commit()
    db.refresh(cycle)
    return cycle

class HabitFactory:
  def create(db: Session, habit_cycle_id: int, **kwargs):
    """Create a habit and save into DB"""
    habit = Habit(
      habit_cycle_id=habit_cycle_id,
      **kwargs
    )

    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

class EntryFactory:
  def create(db: Session, habit_id: int, **kwargs) -> HabitEntry:
    """Create a habit entry and save into DB"""
    defaults = {
      "entry_date": date(2025, 1, 15),
      "completed": False
    }
    defaults.update(kwargs)

    entry = HabitEntry(
      habit_id=habit_id,
      **defaults
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
