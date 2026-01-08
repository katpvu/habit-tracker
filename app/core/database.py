from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(
  DATABASE_URL,
  pool_pre_ping=True,   # Verify connections before using
  pool_size=10,         # Number of connections to maintain
  max_overflow=20,      # Max connections beyond pool_siz
  pool_recycle=3600     # Recycle connections after 1 hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
