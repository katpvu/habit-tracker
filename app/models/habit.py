from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

class Habit(Base):
  __tablename__ = "habits"

  id = Column(Integer, primary_key=True, index=True)
  habit_cycle_id = Column(Integer, ForeignKey("habit_cycles.id", ondelete='CASCADE'), nullable=False, index=True)
  name = Column(String(50), nullable=False)
  created_at = Column(DateTime, default=datetime.now)

  habit_cycle = relationship("HabitCycle", back_populates="habits")
  habit_entries = relationship("HabitEntry", back_populates="habit", order_by="HabitEntry.entry_date.desc()", cascade="all, delete-orphan")

  __table_args__ = (
    UniqueConstraint('habit_cycle_id', 'name', name='uniq_habit_per_cycle'),
  )