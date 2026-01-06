from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from app.core.database import Base

if TYPE_CHECKING:
  from ..models import AuthProvider, HabitCycle
  
class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  created_at = Column(DateTime, nullable=False, default=datetime.now)
  updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  # Relationships

  # User can have multiple auth providers (Discord, Google), and when user is deleted, all their auth providers are deleted too
  auth_providers: Mapped["AuthProvider"] = relationship("AuthProvider", back_populates="user", cascade="all, delete-orphan")

  #User can have multiple habit cycles, and when user is deleted, all habit cycles are also deleted
  habit_cycles: Mapped[List["HabitCycle"]] = relationship("HabitCycle", back_populates="user", cascade="all, delete-orphan")

  