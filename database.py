"""
Database configuration and user management for CodeSense AI
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from logger_config import setup_logging

# Set up logging
logger = setup_logging(__name__)

# Database URL from environment or default
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://samar:admin@localhost:5432/codesense_ai"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()

# Password hashing context with bcrypt compatibility fix
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,  # Explicitly set rounds
    bcrypt__ident="2b"  # Use 2b variant for better compatibility
)

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

# Code Submission model
class CodeSubmission(Base):
    __tablename__ = "code_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to users table
    language = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Path to the stored code file
    analysis_result = Column(String, nullable=True)  # JSON string of analysis results
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    file_name = Column(String, nullable=True)  # Original filename if uploaded

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    # Truncate password to 72 bytes for bcrypt compatibility
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    # Truncate password to 72 bytes for bcrypt compatibility
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

# User management functions
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, password: str, email: str = None, full_name: str = None) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate a user"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    return user

def create_database_and_tables():
    """Create database and tables if they don't exist"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        db = SessionLocal()
        # Try to execute a simple query with explicit text declaration
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

# Code submission management functions
def create_code_submission(db: Session, user_id: int, language: str, file_path: str, 
                          analysis_result: str = None, file_name: str = None) -> CodeSubmission:
    """Create a new code submission record"""
    submission = CodeSubmission(
        user_id=user_id,
        language=language,
        file_path=file_path,
        analysis_result=analysis_result,
        file_name=file_name
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission

def get_user_submissions(db: Session, user_id: int, limit: int = 50) -> List[CodeSubmission]:
    """Get all submissions for a user, ordered by creation date (newest first)"""
    return db.query(CodeSubmission).filter(
        CodeSubmission.user_id == user_id
    ).order_by(CodeSubmission.created_at.desc()).limit(limit).all()

def get_submission_by_id(db: Session, submission_id: int, user_id: int) -> Optional[CodeSubmission]:
    """Get a specific submission by ID, ensuring it belongs to the user"""
    return db.query(CodeSubmission).filter(
        CodeSubmission.id == submission_id,
        CodeSubmission.user_id == user_id
    ).first()

if __name__ == "__main__":
    # Test database connection and create tables
    logger.info("Testing database connection...")
    if test_database_connection():
        logger.info("Creating database tables...")
        create_database_and_tables()
        
        # Test password hashing
        logger.info("Testing password hashing...")
        test_password = "test123"
        hashed = get_password_hash(test_password)
        verified = verify_password(test_password, hashed)
        logger.info(f"Password test: {verified}")
    else:
        logger.error("Please check your PostgreSQL connection settings.")
