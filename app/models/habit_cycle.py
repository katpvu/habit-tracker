from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Enum, Date
from sqlalchemy.orm import relationship, Mapped
from enum import Enum as PyEnum
from datetime import datetime
from typing import TYPE_CHECKING, List
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.habit import Habit
    from app.models.user import User

class CycleTypes(str, PyEnum):
  DAILY = 'daily'
  WEEKLY = 'weekly'
  MONTHLY = 'monthly'
  YEARLY = 'yearly'


class CycleStatuses(str, PyEnum):
  DRAFT = 'draft'
  ACTIVE = 'active'
  COMPLETED = 'completed'
  ABANDONED = 'abandoned'

class HabitCycle(Base):
  """
  Data Model for a Habit Cycle

  
  """
  __tablename__ = "habit_cycles"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  name = Column(String(255), nullable=False)
  cycle_type = Column(Enum(CycleTypes), nullable=False)
  status = Column(Enum(CycleStatuses), nullable=False, default=CycleStatuses.DRAFT)
  created_at = Column(DateTime, nullable=False, default=datetime.now)
  started_at = Column(DateTime)
  completed_at = Column(DateTime)
  updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  # Relationships
  user: Mapped["User"] = relationship("User", back_populates="habit_cycles")
  habits: Mapped[List["Habit"]] = relationship("Habit", back_populates="habit_cycle", cascade="all, delete-orphan", order_by="Habit.created_at.desc()")

  __table_args__ = (
    # Critical constraints:
    # 1. Only one active cycle per type per user
    Index(
      'idx_one_active_cycle_per_type',
      'user_id', 'cycle_type',
      unique=True,
      postgresql_where=(Column('status') == 'ACTIVE')
    ),
  )
