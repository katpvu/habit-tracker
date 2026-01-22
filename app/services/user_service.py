from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User, AuthProvider, Providers


class UserService:
    """Service for user management, particularly Discord user lookup/creation."""

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_user_by_discord_id(self, discord_user_id: str) -> User:
        """
        Look up user by Discord ID, or create new User + AuthProvider if not found.
        Handles concurrent creation race conditions via IntegrityError catch.

        :param discord_user_id: The Discord user's ID (string)
        :return: User object (existing or newly created)
        """
        # Try to find existing AuthProvider for this Discord user
        auth_provider = self._find_discord_auth_provider(discord_user_id)

        if auth_provider:
            return auth_provider.user

        # Create new user + auth provider in transaction
        try:
            return self._create_user_with_discord_auth(discord_user_id)
        except IntegrityError:
            # Concurrent creation - another request created the user
            self.db.rollback()
            auth_provider = self._find_discord_auth_provider(discord_user_id)
            if auth_provider:
                return auth_provider.user
            raise  # Re-raise if still not found (unexpected)

    def _find_discord_auth_provider(self, discord_user_id: str) -> Optional[AuthProvider]:
        """Query AuthProvider by Discord provider and user ID."""
        return self.db.query(AuthProvider).filter(
            AuthProvider.provider == Providers.DISCORD,
            AuthProvider.provider_user_id == discord_user_id
        ).first()

    def _create_user_with_discord_auth(self, discord_user_id: str) -> User:
        """Create User and linked AuthProvider in a single transaction."""
        # Create minimal user (just timestamps, which have defaults)
        user = User()
        self.db.add(user)
        self.db.flush()  # Get user.id without committing

        # Create AuthProvider linking to Discord
        auth_provider = AuthProvider(
            user_id=user.id,
            provider=Providers.DISCORD,
            provider_user_id=discord_user_id
        )
        self.db.add(auth_provider)
        self.db.commit()
        self.db.refresh(user)

        return user
