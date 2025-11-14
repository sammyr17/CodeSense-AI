"""
Unit tests for auth.py
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from auth import (
    create_access_token, verify_token, get_current_user,
    UserLogin, UserSignup, UserResponse, Token,
    SECRET_KEY, ALGORITHM
)


class TestJWTUtilities:
    """Test JWT token utilities"""
    
    def test_create_access_token_default_expiry(self):
        """Test creating access token with default expiry"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        # Decode token to verify
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "testuser"
        assert "exp" in payload
    
    def test_create_access_token_custom_expiry(self):
        """Test creating access token with custom expiry"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=60)
        token = create_access_token(data, expires_delta)
        
        # Decode token to verify
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "testuser"
        
        # Check expiry is approximately 60 minutes from now
        exp_time = datetime.utcfromtimestamp(payload["exp"])
        expected_time = datetime.utcnow() + expires_delta
        time_diff = abs((exp_time - expected_time).total_seconds())
        assert time_diff < 5  # Allow 5 second difference
    
    def test_verify_token_valid(self):
        """Test verifying valid token"""
        # Create token
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        # Create credentials object
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        # Verify token
        username = verify_token(credentials)
        assert username == "testuser"
    
    def test_verify_token_invalid(self):
        """Test verifying invalid token"""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid_token"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(credentials)
        
        assert exc_info.value.status_code == 401
    
    def test_verify_token_expired(self):
        """Test verifying expired token"""
        # Create expired token
        data = {"sub": "testuser"}
        expires_delta = timedelta(seconds=-1)  # Already expired
        token = create_access_token(data, expires_delta)
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(credentials)
        
        assert exc_info.value.status_code == 401
    
    def test_verify_token_no_subject(self):
        """Test verifying token without subject"""
        # Create token without 'sub' field
        data = {"user": "testuser"}  # Wrong field name
        token = create_access_token(data)
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(credentials)
        
        assert exc_info.value.status_code == 401


class TestGetCurrentUser:
    """Test get_current_user function"""
    
    @patch('auth.get_user_by_username')
    def test_get_current_user_success(self, mock_get_user, test_db):
        """Test successful user retrieval"""
        # Mock user
        mock_user = Mock()
        mock_user.username = "testuser"
        mock_get_user.return_value = mock_user
        
        # Get current user
        user = get_current_user("testuser", test_db)
        
        assert user == mock_user
        mock_get_user.assert_called_once_with(test_db, username="testuser")
    
    @patch('auth.get_user_by_username')
    def test_get_current_user_not_found(self, mock_get_user, test_db):
        """Test user not found"""
        mock_get_user.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user("nonexistent", test_db)
        
        assert exc_info.value.status_code == 401


class TestPydanticModels:
    """Test Pydantic models"""
    
    def test_user_login_model(self):
        """Test UserLogin model"""
        login_data = UserLogin(username="testuser", password="testpass123")
        
        assert login_data.username == "testuser"
        assert login_data.password == "testpass123"
    
    def test_user_signup_model(self):
        """Test UserSignup model"""
        signup_data = UserSignup(
            username="testuser",
            password="testpass123",
            email="test@example.com",
            full_name="Test User"
        )
        
        assert signup_data.username == "testuser"
        assert signup_data.password == "testpass123"
        assert signup_data.email == "test@example.com"
        assert signup_data.full_name == "Test User"
    
    def test_user_signup_model_optional_fields(self):
        """Test UserSignup model with optional fields"""
        signup_data = UserSignup(username="testuser", password="testpass123")
        
        assert signup_data.username == "testuser"
        assert signup_data.password == "testpass123"
        assert signup_data.email is None
        assert signup_data.full_name is None
    
    def test_user_response_model(self):
        """Test UserResponse model"""
        now = datetime.utcnow()
        user_response = UserResponse(
            id=1,
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            is_active=True,
            created_at=now,
            last_login=now
        )
        
        assert user_response.id == 1
        assert user_response.username == "testuser"
        assert user_response.email == "test@example.com"
        assert user_response.full_name == "Test User"
        assert user_response.is_active is True
        assert user_response.created_at == now
        assert user_response.last_login == now
    
    def test_token_model(self):
        """Test Token model"""
        user_response = UserResponse(
            id=1,
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            is_active=True,
            created_at=datetime.utcnow(),
            last_login=None
        )
        
        token = Token(
            access_token="test_token",
            token_type="bearer",
            user=user_response
        )
        
        assert token.access_token == "test_token"
        assert token.token_type == "bearer"
        assert token.user == user_response
