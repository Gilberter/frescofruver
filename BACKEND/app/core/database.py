import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# 1. Define a local fallback path
LOCAL_DB_URL = "sqlite:///./local_database.db"

def create_db_engine():
    try:
        print("Connecting to:", settings.DATABASE_URL)

        temp_engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=settings.is_dev,
        )

        with temp_engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        print("Connected to MySQL successfully!")
        return temp_engine

    except Exception as e:
        print("MySQL connection failed:")
        print(e)

        print("Falling back to SQLite...")
        return create_engine(
            LOCAL_DB_URL,
            connect_args={"check_same_thread": False}
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
