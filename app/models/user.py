from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  created_at = Column(DateTime, nullable=False, default=datetime.now)
  updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  # Relationships

  