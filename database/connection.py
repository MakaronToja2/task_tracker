from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables - drops existing ones to handle schema changes"""
    # For development, we'll drop and recreate tables to handle schema changes
    # In production, you'd use Alembic migrations instead
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)