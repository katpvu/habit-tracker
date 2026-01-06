from typing import TYPE_CHECKING, List
from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime

if TYPE_CHECKING:
    from ..models import HabitCycle, HabitEntry

class Habit(Base):
  __tablename__ = "habits"

  id = Column(Integer, primary_key=True, index=True)
  habit_cycle_id = Column(Integer, ForeignKey("habit_cycles.id", ondelete='CASCADE'), nullable=False, index=True)
  name = Column(String(50), nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  habit_cycle: Mapped["HabitCycle"] = relationship("HabitCycle", back_populates="habits")
  habit_entries: Mapped[List["HabitEntry"]] = relationship("HabitEntry", back_populates="habit", order_by="HabitEntry.entry_date.desc()", cascade="all, delete-orphan")

  __table_args__ = (
    UniqueConstraint('habit_cycle_id', 'name', name='uniq_habit_per_cycle'),
  )