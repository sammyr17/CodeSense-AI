"""
Unit tests for database.py
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from database import (
    User, CodeSubmission, get_password_hash, verify_password,
    create_user, authenticate_user, get_user_by_username, get_user_by_email,
    create_code_submission, get_user_submissions, get_submission_by_id,
    test_database_connection, create_database_and_tables
)


class TestPasswordUtilities:
    """Test password hashing and verification"""
    
    def test_password_hashing(self):
        """Test password hashing"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert verify_password(password, hashed)
    
    def test_password_verification_failure(self):
        """Test password verification with wrong password"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert not verify_password(wrong_password, hashed)
    
    def test_long_password_truncation(self):
        """Test that long passwords are truncated for bcrypt compatibility"""
        long_password = "a" * 100  # 100 characters
        hashed = get_password_hash(long_password)
        
        # Should still work with truncated password
        assert verify_password(long_password, hashed)


class TestUserModel:
    """Test User model and related functions"""
    
    def test_user_creation(self, test_db):
        """Test creating a new user"""
        user = create_user(
            db=test_db,
            username="testuser",
            password="testpass123",
            email="test@example.com",
            full_name="Test User"
        )
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.hashed_password != "testpass123"
        assert user.id is not None
    
    def test_get_user_by_username(self, test_db):
        """Test retrieving user by username"""
        # Create user
        create_user(test_db, "testuser", "testpass123", "test@example.com")
        
        # Retrieve user
        user = get_user_by_username(test_db, "testuser")
        assert user is not None
        assert user.username == "testuser"
        
        # Test non-existent user
        user = get_user_by_username(test_db, "nonexistent")
        assert user is None
    
    def test_get_user_by_email(self, test_db):
        """Test retrieving user by email"""
        # Create user
        create_user(test_db, "testuser", "testpass123", "test@example.com")
        
        # Retrieve user
        user = get_user_by_email(test_db, "test@example.com")
        assert user is not None
        assert user.email == "test@example.com"
        
        # Test non-existent email
        user = get_user_by_email(test_db, "nonexistent@example.com")
        assert user is None
    
    def test_authenticate_user_success(self, test_db):
        """Test successful user authentication"""
        # Create user
        create_user(test_db, "testuser", "testpass123", "test@example.com")
        
        # Authenticate
        user = authenticate_user(test_db, "testuser", "testpass123")
        assert user is not None
        assert user.username == "testuser"
        assert user.last_login is not None
    
    def test_authenticate_user_failure(self, test_db):
        """Test failed user authentication"""
        # Create user
        create_user(test_db, "testuser", "testpass123", "test@example.com")
        
        # Test wrong password
        user = authenticate_user(test_db, "testuser", "wrongpass")
        assert user is None
        
        # Test non-existent user
        user = authenticate_user(test_db, "nonexistent", "testpass123")
        assert user is None


class TestCodeSubmissionModel:
    """Test CodeSubmission model and related functions"""
    
    def test_create_code_submission(self, test_db):
        """Test creating a code submission"""
        # Create user first
        user = create_user(test_db, "testuser", "testpass123", "test@example.com")
        
        # Create submission
        submission = create_code_submission(
            db=test_db,
            user_id=user.id,
            language="python",
            file_path="/tmp/test.py",
            analysis_result='{"test": "result"}',
            file_name="test.py"
        )
        
        assert submission.user_id == user.id
        assert submission.language == "python"
        assert submission.file_path == "/tmp/test.py"
        assert submission.analysis_result == '{"test": "result"}'
        assert submission.file_name == "test.py"
        assert submission.id is not None
        assert submission.created_at is not None
    
    def test_get_user_submissions(self, test_db):
        """Test retrieving user submissions"""
        # Create user
        user = create_user(test_db, "testuser", "testpass123", "test@example.com")
        
        # Create multiple submissions
        submission1 = create_code_submission(test_db, user.id, "python", "/tmp/test1.py")
        submission2 = create_code_submission(test_db, user.id, "javascript", "/tmp/test2.js")
        
        # Get submissions
        submissions = get_user_submissions(test_db, user.id)
        
        assert len(submissions) == 2
        # Check that both submissions are present (order may vary due to timing)
        submission_ids = [s.id for s in submissions]
        assert submission1.id in submission_ids
        assert submission2.id in submission_ids
    
    def test_get_submission_by_id(self, test_db):
        """Test retrieving specific submission"""
        # Create user
        user = create_user(test_db, "testuser", "testpass123", "test@example.com")
        
        # Create submission
        submission = create_code_submission(test_db, user.id, "python", "/tmp/test.py")
        
        # Retrieve submission
        retrieved = get_submission_by_id(test_db, submission.id, user.id)
        assert retrieved is not None
        assert retrieved.id == submission.id
        
        # Test with wrong user_id
        retrieved = get_submission_by_id(test_db, submission.id, 999)
        assert retrieved is None
        
        # Test with non-existent submission
        retrieved = get_submission_by_id(test_db, 999, user.id)
        assert retrieved is None


class TestDatabaseUtilities:
    """Test database utility functions"""
    
    @patch('database.SessionLocal')
    def test_database_connection_success(self, mock_session):
        """Test successful database connection"""
        mock_db = Mock()
        mock_session.return_value = mock_db
        
        result = test_database_connection()
        assert result is True
        mock_db.execute.assert_called_once()
        mock_db.close.assert_called_once()
    
    @patch('database.SessionLocal')
    def test_database_connection_failure(self, mock_session):
        """Test failed database connection"""
        mock_session.side_effect = Exception("Connection failed")
        
        result = test_database_connection()
        assert result is False
    
    @patch('database.Base.metadata.create_all')
    def test_create_database_and_tables_success(self, mock_create_all):
        """Test successful database table creation"""
        result = create_database_and_tables()
        assert result is True
        mock_create_all.assert_called_once()
    
    @patch('database.Base.metadata.create_all')
    def test_create_database_and_tables_failure(self, mock_create_all):
        """Test failed database table creation"""
        mock_create_all.side_effect = Exception("Creation failed")
        
        result = create_database_and_tables()
        assert result is False
