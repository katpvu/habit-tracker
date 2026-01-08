import pytest
from sqlalchemy.exc import IntegrityError

from tests.fixtures.factories import CycleFactory, EntryFactory

def test_unique_active_cycle_constraint(db_session, test_user):
  """
  Test database prevents multiple active cycles of the same type per user

  Table: habit_cycles
  """
  from app.models import CycleTypes, CycleStatuses
  
  cycle_properties = {
    "cycle_type": CycleTypes.DAILY,
    "status": CycleStatuses.ACTIVE
  }
  
  # Create active cycle
  CycleFactory.create(
    db=db_session,
    user_id=test_user.id,
    name="Active Cycle",
    **cycle_properties
  )

  # This block should fail due to unique constraint
  with pytest.raises(IntegrityError):
    # Try to create another active cycle
    CycleFactory.create(
      db=db_session,
      user_id=test_user.id,
      name="Second Active Cycle",
      **cycle_properties
    )

def test_unique_entry_constraint(db_session, test_user):
  """
  Test database prevents multiple entries for the same habit on the same day.

  Table: habit_entries
  Unique constraint on habit_id and entry_date
  """
  active_cycle = CycleFactory.create_with_habits(
    db=db_session,
    user_id=test_user.id
  )

  habit = active_cycle.habits[0]

  EntryFactory.create(
    db=db_session,
    habit_id=habit.id,
    completed=True
  )

  with pytest.raises(IntegrityError):
    EntryFactory.create(
      db=db_session,
      habit_id=habit.id,
      completed=True
    )
