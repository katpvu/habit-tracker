from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, Date, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime

if TYPE_CHECKING:
    from ..models.habit import Habit
    
class HabitEntry(Base):
  __tablename__ = "habit_entries"

  id = Column(Integer, primary_key=True, index=True)
  habit_id = Column(Integer, ForeignKey('habits.id', ondelete='CASCADE'), nullable=False)
  entry_date = Column(Date, nullable=False, index=True)
  completed = Column(Boolean, nullable=False, default=False)
  completed_at = Column(DateTime, nullable=True) # Only set when completed
  created_at = Column(DateTime, default=datetime.now)

  habit: Mapped["Habit"] = relationship("Habit", back_populates="habit_entries")

  __table_args__ = (
    # Disables users from submitting another entry for the same habit in the same day
    UniqueConstraint('habit_id', 'entry_date', name='uniq_habit_entry_date'),
  )

  def mark_complete(self):
     """Mark this entry as completed"""
     self.completed = True
     self.completed_at = datetime.now()

