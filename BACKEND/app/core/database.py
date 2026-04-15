from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # reconnect on stale connections
    pool_recycle=3600,        # recycle connections every hour
    echo=settings.is_dev,     # log SQL only in dev
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


def get_db():
    """Yield a database session and ensure it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
