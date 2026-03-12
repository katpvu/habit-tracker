from app.services.oauth.base import BaseOAuthProvider
from app.core.config import settings
import httpx

CLIENT_ID = settings.DISCORD_CLIENT_ID
CLIENT_SECRET = settings.DISCORD_CLIENT_SECRET
REDIRECT_URI = settings.DISCORD_REDIRECT_URI
AUTHORIZATION_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=identify+email"

class DiscordOAuthProvider(BaseOAuthProvider):

  def get_authorization_url(self):
    super().get_authorization_url()

  def exchange_code_for_token(self, code):
    super().exchange_code_for_token(code)
  

