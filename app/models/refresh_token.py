from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from app.core.database import Base


if TYPE_CHECKING:
    from ..models import User
    
class RefreshToken(Base):
    """
    Refresh tokens for maintaining user sessions.

    When a user logs in via OAuth, we generate:
    1. A short-lived JWT (15 min) - sent to client, NOT stored
    2. A long-lived refresh token (30 days) - stored here

    Client uses refresh token to get new JWTs without re-authenticating.
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(500), unique=True, nullable=False, index=True)  # Random token string
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)  # For manual revocation
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Optional: Track what created this token
    user_agent = Column(String(500), nullable=True)  # "Discord Bot" or "CLI v1.0"
    ip_address = Column(String(50), nullable=True)   # For security monitoring

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")

    __table_args__ = (
        Index('idx_user_active_tokens', 'user_id', 'revoked', 'expires_at'),
    )
