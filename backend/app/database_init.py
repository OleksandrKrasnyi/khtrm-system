#!/usr/bin/env python3
"""
Database initialization script for KHTRM System
Creates tables and initial data for MySQL in Docker container
"""

import logging

from sqlalchemy import text

from app.database import engine, get_db
from app.models.base import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables() -> bool:
    """Create all tables in the database"""
    try:
        # Create tables using SQLAlchemy
        Base.metadata.create_all(bind=engine)

        logger.info("✅ Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False


def insert_initial_data() -> bool:
    """Insert initial data into the database"""
    try:
        # Use synchronous session for mock data creation
        from .mock_data.dispatcher_mock_data import create_all_mock_data  # type: ignore

        # Get synchronous database session
        db_gen = get_db()
        db = next(db_gen)

        try:
            # Create mock data for dispatcher functionality
            create_all_mock_data(db)
            logger.info("✅ Initial data and mock data inserted successfully")
            return True
        finally:
            db.close()

    except Exception as e:
        logger.error(f"❌ Error inserting initial data: {e}")
        return False


def check_database_connection() -> bool:
    """Check if database connection is working"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row and row[0] == 1:
                logger.info("✅ Database connection successful")
                return True
            else:
                logger.error("❌ Database connection failed")
                return False
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False


def initialize_database() -> bool:
    """Main initialization function"""
    logger.info("🚀 Starting database initialization...")

    # Check connection
    if not check_database_connection():
        logger.error("❌ Cannot connect to database")
        return False

    # Create tables
    if not create_tables():
        logger.error("❌ Failed to create tables")
        return False

    # Insert initial data
    if not insert_initial_data():
        logger.error("❌ Failed to insert initial data")
        return False

    logger.info("🎉 Database initialization completed successfully!")
    return True


if __name__ == "__main__":
    initialize_database()
