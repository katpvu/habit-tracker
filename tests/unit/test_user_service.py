import pytest
from app.services.user_service import UserService
from app.models import AuthProvider, Providers
from tests.fixtures.factories import UserFactory, AuthProviderFactory


class TestUserService:
    """Tests for UserService"""

    def test_get_or_create_creates_new_user(self, db_session):
        """When Discord user doesn't exist, create new User + AuthProvider"""
        service = UserService(db_session)
        discord_id = "new_discord_user_123"

        user = service.get_or_create_user_by_discord_id(discord_id)

        assert user is not None
        assert user.id is not None

        # Verify AuthProvider was created
        auth_provider = db_session.query(AuthProvider).filter(
            AuthProvider.provider == Providers.DISCORD,
            AuthProvider.provider_user_id == discord_id
        ).first()

        assert auth_provider is not None
        assert auth_provider.user_id == user.id

    def test_get_or_create_returns_existing_user(self, db_session):
        """When Discord user exists, return existing User"""
        # Create existing user with Discord auth
        existing_user = UserFactory.create(db_session)
        discord_id = "existing_discord_456"
        AuthProviderFactory.create(
            db_session,
            user_id=existing_user.id,
            provider=Providers.DISCORD,
            provider_user_id=discord_id
        )

        service = UserService(db_session)
        user = service.get_or_create_user_by_discord_id(discord_id)

        assert user.id == existing_user.id

    def test_get_or_create_different_discord_ids_different_users(self, db_session):
        """Different Discord IDs create different users"""
        service = UserService(db_session)

        user1 = service.get_or_create_user_by_discord_id("discord_111")
        user2 = service.get_or_create_user_by_discord_id("discord_222")

        assert user1.id != user2.id

    def test_get_or_create_same_discord_id_same_user(self, db_session):
        """Same Discord ID always returns the same user"""
        service = UserService(db_session)
        discord_id = "consistent_discord_789"

        user1 = service.get_or_create_user_by_discord_id(discord_id)
        user2 = service.get_or_create_user_by_discord_id(discord_id)

        assert user1.id == user2.id

    def test_created_user_has_correct_provider(self, db_session):
        """New user has AuthProvider with DISCORD provider type"""
        service = UserService(db_session)
        discord_id = "provider_test_123"

        user = service.get_or_create_user_by_discord_id(discord_id)

        # Check the auth provider
        auth_provider = db_session.query(AuthProvider).filter(
            AuthProvider.user_id == user.id
        ).first()

        assert auth_provider.provider == Providers.DISCORD
        assert auth_provider.provider_user_id == discord_id
