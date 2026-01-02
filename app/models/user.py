from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  created_at = Column(DateTime, nullable=False, default=datetime.now)
  updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  # Relationships

  # User can have multiple auth providers (Discord, Google), and when user is deleted, all their auth providers are deleted too
  auth_providers = relationship("AuthProvider", back_populates="user", cascade="all, delete-orphan")

  #User can have multiple habit cycles, and when user is deleted, all habit cycles are also deleted
  habit_cycles = relationship("HabitCycle", back_populates="user", cascade="all, delete-orphan")

  