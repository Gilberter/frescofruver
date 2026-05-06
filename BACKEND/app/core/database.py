import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# 1. Define a local fallback path
LOCAL_DB_URL = "sqlite:///./local_database.db"

def create_db_engine():
    try:
        # Try primary database (e.g., MySQL from .env)
        temp_engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=settings.is_dev,
        )
        # Test connection immediately
        with temp_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return temp_engine
    except Exception:
        print("⚠️ Primary DB connection failed. Falling back to local SQLite.")
        # 2. Fallback to local SQLite if primary fails
        return create_engine(
            LOCAL_DB_URL,
            connect_args={"check_same_thread": False} # Needed for SQLite + FastAPI
        )

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

def validate_database_connection() -> None:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        # This will now only raise if even the local SQLite fails
        raise RuntimeError("No se pudo conectar a ninguna base de datos (Principal ni Local).") from exc

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
