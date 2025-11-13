"""
Database setup script for CodeSense AI
Run this script to create the database and tables
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database import create_database_and_tables, test_database_connection
from logger_config import setup_logging

# Set up logging
logger = setup_logging(__name__)

def create_database():
    """Create the codesense_ai database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="samar",
            password="admin"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='codesense_ai'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE codesense_ai")
            logger.info("Database 'codesense_ai' created successfully")
        else:
            logger.info("Database 'codesense_ai' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    logger.info("Setting up CodeSense AI database...")
    
    # Step 1: Create database
    if create_database():
        # Step 2: Test connection
        if test_database_connection():
            # Step 3: Create tables
            create_database_and_tables()
            logger.info("Database setup completed successfully!")
        else:
            logger.error("Failed to connect to database")
    else:
        logger.error("Failed to create database")
