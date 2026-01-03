from datetime import timedelta, datetime
import jwt
from app.core.config import settings

def create_access_token(user_id: int) -> str:
  """
  Creates JWT token
  
  :param user_id: The user's ID 
  :param user_id: int
  :return: JWT token
  :rtype: str
  """
  payload = {
    "sub": str(user_id),
    "exp": datetime.now() + timedelta(days=365),
    "iat": datetime.now()
  }

  return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

def verify_access_token(token: str) -> dict:
  """
  Verify and decode JWT token
  
  :param token: JWT token
  :type token: str
  :return: Decoded payload with user_id
  :rtype: dict
  """
  return jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)