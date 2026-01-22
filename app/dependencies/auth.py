from typing import Optional
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import verify_access_token
from app.core.database import get_db
from app.models.user import User
from app.services.user_service import UserService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get user from JWT token. Used for direct user authentication."""
    token = credentials.credentials
    payload = verify_access_token(token)
    user_id = int(payload["sub"])

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


async def get_discord_user(
    discord_user_id: Optional[str] = Query(None, description="Discord user ID"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Resolve user from bot request.

    1. Verify JWT is valid (bot authentication)
    2. If discord_user_id provided, look up/create Discord user
    3. If no discord_user_id, return the JWT's user (backward compatibility)
    """
    # Verify the JWT token
    token = credentials.credentials
    payload = verify_access_token(token)
    jwt_user_id = int(payload["sub"])

    # If discord_user_id provided, resolve to Discord user
    if discord_user_id:
        user_service = UserService(db)
        return user_service.get_or_create_user_by_discord_id(discord_user_id)

    # Fallback: return the JWT's user (bot user or direct auth)
    user = db.query(User).filter(User.id == jwt_user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
