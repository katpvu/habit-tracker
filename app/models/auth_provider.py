from sqlalchemy import Column, Integer, DateTime, Enum, String, Index
from enum import Enum as PyEnum
from app.core.database import Base

class Providers(PyEnum):
  GOOGLE = 'google'
  DISCORD = 'discord'

class AuthProvider(Base):
  __tablename__ = "auth_providers"

  id = Column(Integer, primary_key=True, index=True)
  provider = Column(Enum(Providers), nullable=False)
  provider_id = Column(String(255), unique=False, nullable=False)
  access_token = Column(String(500), nullable=True) # For OAuth
  refresh_token = Column(String(500), nullable=True)

  __table_args__ = (
    Index('idx_provider_user', 'provider', 'provider_id', unique=True),
  )

