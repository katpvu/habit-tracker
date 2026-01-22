import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, get_db
from app.models.user import User
from app.models.auth_provider import AuthProvider, Providers
from app.core.security import create_access_token

def create_bot_user():
  db = SessionLocal()
  try:
    # Check if bot user already exists
    existing_bot_user = db.query(AuthProvider).filter(AuthProvider.provider == Providers.DISCORD_BOT).first()
    if existing_bot_user:
      print(f"Bot user already exists! Bot UserID: {existing_bot_user.user_id}")
      return
    
    print("Creating bot user...")
    bot_user = User()
    db.add(bot_user)
    db.flush()

    bot_auth = AuthProvider(
      user_id=bot_user.id,
      provider=Providers.DISCORD_BOT,
      provider_user_id="discord_bot_service"
    )

    db.add(bot_auth)
    db.commit()

    bot_jwt = create_access_token(
      user_id=bot_user.id
    )

    print("✅ Bot user created successfully!")
    print(f"\nBot User ID: {bot_user.id}")
    print(f"\nBot JWT (save this!):\n{bot_jwt}")
    print(f"\n" + "="*60)
    print("Add this to your Discord bot's .env file:")
    print("="*60)
    print(f"BOT_JWT={bot_jwt}")
    print("="*60)

  except Exception as e:
      print(f"Error creating bot user: {e}")
      db.rollback()
  finally:
      db.close()

if __name__ == "__main__":
   create_bot_user()