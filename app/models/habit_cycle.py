from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Enum, Date
from enum import Enum as PyEnum
from datetime import datetime
from app.core.database import Base

class CycleTypes(PyEnum):
  DAILY = 'daily'
  WEEKLY = 'weekly'
  MONTHLY = 'monthly'
  YEARLY = 'yearly'


class CycleStatuses(PyEnum):
  DRAFT = 'draft'
  ACTIVE = 'active'
  COMPLETED = 'completed'
  ABANDONED = 'abandoned'

class HabitCycle(Base):
  __tablename__ = "habit_cycles"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  name = Column(String(255), nullable=False)
  cycle_type = Column(Enum(CycleTypes), nullable=False)
  status = Column(Enum(CycleStatuses), nullable=False, default=CycleStatuses.DRAFT)
  created_at = Column(DateTime, nullable=False, default=datetime.now)
  started_at = Column(DateTime)
  completed_at = Column(DateTime)

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
