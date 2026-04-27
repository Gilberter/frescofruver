from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

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


def validate_database_connection() -> None:
    """Open a connection and run a trivial query.

    Raises:
        RuntimeError: When the DB connection fails, with a clearer message.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise RuntimeError(
            "No se pudo conectar a MySQL usando DATABASE_URL. "
            "Revisa BACKEND/.env, el driver PyMySQL y que el usuario MySQL "
            "permita el plugin de autenticacion configurado."
        ) from exc


def get_db():
    """Yield a database session and ensure it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
