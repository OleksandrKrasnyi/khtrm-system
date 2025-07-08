"""Database configuration and connection setup."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings
from .models.base import Base

# Create database engine
engine = create_engine(
    settings.effective_database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
    # SQLite specific settings
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.effective_database_url
    else {},
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)
    print("📊 Database tables created successfully")


def get_db():
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database utility functions
def init_db():
    """Initialize database with tables."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)


def reset_db():
    """Reset database (drop and recreate tables)."""
    drop_db()
    init_db()
