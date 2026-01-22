from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseOAuthProvider(ABC):
  """
  Abstract base for OAuth providers
  Each provider implements how to talk to their specific API.
  """

  @abstractmethod
  def get_authorization_url(self) -> str:
    """Return the OAuth authorization URL for this provider"""
    pass

  @abstractmethod
  async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
    """
    Exchange authorization code for access token.
    
    :param self: Description
    :param code: Description
    :type code: str
    :return: Access token as a result of exchanging authorization code
    :rtype: Dict[str, Any]
    """
    pass

  