from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, DateTime, Enum, String, Index, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from enum import Enum as PyEnum
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User

class Providers(PyEnum):
  GOOGLE = 'google'
  DISCORD = 'discord'
  DISCORD_BOT = 'dicord_bot'

class AuthProvider(Base):
  __tablename__ = "auth_providers"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
  provider = Column(Enum(Providers), nullable=False)
  provider_user_id = Column(String(255), unique=False, nullable=False)
  access_token = Column(String(500), nullable=True) # For OAuth
  refresh_token = Column(String(500), nullable=True)
  token_expires_at = Column(DateTime, nullable=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  # Relationships
  user: Mapped["User"] = relationship("User", back_populates="auth_providers")

  __table_args__ = (
    Index('idx_provider_user_unique', 'provider', 'provider_user_id', unique=True),
    Index('idx_user_providers', 'user_id'),
  )

