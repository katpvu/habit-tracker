# Shared fixtures - reusable setup/teardown code that prepares the environment for tests and cleanup.
# They create objects, data, or state that multiple tests need

# Common uses: 
# 1. Database setup: create test DB, populate with sample data
# 2. Mock objects: Pre-configured fake services/APIs
# 3. Test data: Users, habits, entries to test against
# 4. Configuration: Test-specific settings
# 5. Cleanup: Reset state after each test

from typing import Any, Generator
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.main import app
from app.models import User, HabitCycle, Habit
from app.core.security import create_access_token

# Database fixtures
@pytest.fixture(scope="function")
def db_session() -> Generator[Session, Any, None]:
  """Create a fresh database for each test"""
  # Use in-memory SQLite for speed
  engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
  )

  Base.metadata.create_all(bind=engine) # Creates all the tables
  TestingSessionLocal = sessionmaker(bind=engine)
  db = TestingSessionLocal()

  yield db

  db.close()
  Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
  """
  Create a new FastAPI TestClient that uses the `db_session` fixture to override
  the `get_db` dependency that is injected into routes.
  """
  def _get_test_db():
    try:
      yield db_session
    finally:
      pass

  app.dependency_overrides[get_db] = _get_test_db

  with TestClient(app) as test_client:
    yield test_client

  app.dependency_overrides.clear()

# Model fixtures
@pytest.fixture
def test_user(db_session):
  """Create test user"""
  user = User()
  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)
  return user

@pytest.fixture
def test_cycle(db_session, test_user):
  """Create a test cycle"""
  from app.models import CycleTypes, CycleStatuses
  cycle = HabitCycle(
    user_id=test_user.id,
    name="Test Cycle",
    cycle_type=CycleTypes.DAILY,
    status=CycleStatuses.DRAFT
  )
  db_session.add(cycle)
  db_session.commit()
  db_session.refresh(cycle)
  return cycle

@pytest.fixture
def test_habit(db_session, test_cycle):
  """Create a test habit"""
  habit = Habit(
    name="Test habit",
    habit_cycle_id=test_cycle.id
  )

  db_session.add(habit)
  db_session.commit()
  db_session.refresh(habit)
  return habit

# Auth fixtures
@pytest.fixture
def auth_headers(test_user):
  """Generate auth headers with JWT"""
  token = create_access_token(data={"sub": str(test_user.id)})
  return {"Authorization": f"Bearer {token}"}