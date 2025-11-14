"""
API Integration Tests for CodeSense AI
Tests the complete API workflows end-to-end
"""
import pytest
import requests
import json
import time
from unittest.mock import patch


class TestAPIIntegration:
    """Integration tests for the complete API workflow"""
    
    BASE_URL = "http://localhost:8000"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for integration tests"""
        self.session = requests.Session()
        self.user_token = None
        self.test_user = {
            "username": f"testuser_{int(time.time())}",
            "password": "testpass123",
            "email": f"test_{int(time.time())}@example.com",
            "full_name": "Test User"
        }
    
    def test_user_registration_and_login_flow(self):
        """Test complete user registration and login flow"""
        # 1. Register new user
        signup_response = self.session.post(
            f"{self.BASE_URL}/auth/signup",
            json=self.test_user
        )
        
        assert signup_response.status_code == 200
        signup_data = signup_response.json()
        assert "access_token" in signup_data
        assert "user" in signup_data
        assert signup_data["user"]["username"] == self.test_user["username"]
        
        # Store token for subsequent requests
        self.user_token = signup_data["access_token"]
        self.session.headers.update({
            "Authorization": f"Bearer {self.user_token}"
        })
        
        # 2. Test login with same credentials
        login_response = self.session.post(
            f"{self.BASE_URL}/auth/login",
            json={
                "username": self.test_user["username"],
                "password": self.test_user["password"]
            }
        )
        
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data
        
        # 3. Get current user info
        me_response = self.session.get(f"{self.BASE_URL}/auth/me")
        
        assert me_response.status_code == 200
        user_data = me_response.json()
        assert user_data["username"] == self.test_user["username"]
        assert user_data["email"] == self.test_user["email"]
    
    def test_duplicate_user_registration(self):
        """Test that duplicate user registration fails"""
        # First registration
        signup_response1 = self.session.post(
            f"{self.BASE_URL}/auth/signup",
            json=self.test_user
        )
        assert signup_response1.status_code == 200
        
        # Duplicate registration should fail
        signup_response2 = self.session.post(
            f"{self.BASE_URL}/auth/signup",
            json=self.test_user
        )
        assert signup_response2.status_code == 400
        assert "already registered" in signup_response2.json()["detail"]
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        login_response = self.session.post(
            f"{self.BASE_URL}/auth/login",
            json={
                "username": "nonexistent_user",
                "password": "wrongpassword"
            }
        )
        
        assert login_response.status_code == 401
        assert "Incorrect username or password" in login_response.json()["detail"]
    
    @patch('app.docker_executor.execute_code')
    @patch('app.genai.GenerativeModel')
    def test_complete_code_analysis_workflow(self, mock_model_class, mock_docker_execute):
        """Test complete code analysis workflow"""
        # Setup authentication
        self._authenticate()
        
        # Mock Docker execution
        mock_docker_execute.return_value = {
            'stdout': 'Hello, World!\nNumber: 0\nNumber: 1\nNumber: 2',
            'stderr': '',
            'exit_code': 0,
            'execution_time': 1.2,
            'error': None
        }
        
        # Mock Gemini response
        mock_model = mock_model_class.return_value
        mock_response = type('MockResponse', (), {
            'text': json.dumps({
                "errors": [],
                "suggestions": ["Consider adding error handling", "Use more descriptive variable names"],
                "optimizations": ["Code looks good", "Consider using list comprehension"],
                "output": "Code successfully prints greeting and numbers 0-2",
                "quality_metrics": {
                    "summary": "Good code quality with simple logic",
                    "complexity_issues": [],
                    "security_issues": [],
                    "recommendations": ["Add docstrings", "Consider type hints"],
                    "security_analysis": "No security issues detected"
                }
            }),
            'candidates': [type('MockCandidate', (), {'finish_reason': 1})()]
        })()
        mock_model.generate_content.return_value = mock_response
        
        # Test code analysis
        code_data = {
            "code": "print('Hello, World!')\nfor i in range(3):\n    print(f'Number: {i}')",
            "language": "python"
        }
        
        analysis_response = self.session.post(
            f"{self.BASE_URL}/api/analyze",
            json=code_data
        )
        
        assert analysis_response.status_code == 200
        analysis_data = analysis_response.json()
        
        # Verify response structure
        assert "errors" in analysis_data
        assert "suggestions" in analysis_data
        assert "optimizations" in analysis_data
        assert "output" in analysis_data
        assert "code_output" in analysis_data
        assert "execution_success" in analysis_data
        assert "quality_metrics" in analysis_data
        
        # Verify execution results
        assert analysis_data["execution_success"] is True
        assert "Hello, World!" in analysis_data["code_output"]
        assert "Number: 0" in analysis_data["code_output"]
        
        # Verify AI analysis
        assert len(analysis_data["suggestions"]) > 0
        assert len(analysis_data["optimizations"]) > 0
    
    def test_code_analysis_without_auth(self):
        """Test that code analysis requires authentication"""
        code_data = {
            "code": "print('Hello, World!')",
            "language": "python"
        }
        
        response = self.session.post(
            f"{self.BASE_URL}/api/analyze",
            json=code_data
        )
        
        assert response.status_code == 403
    
    def test_submission_history_workflow(self):
        """Test submission history workflow"""
        # Setup authentication
        self._authenticate()
        
        # Get initial submissions (should be empty)
        submissions_response = self.session.get(f"{self.BASE_URL}/api/submissions")
        assert submissions_response.status_code == 200
        initial_submissions = submissions_response.json()["submissions"]
        initial_count = len(initial_submissions)
        
        # Perform code analysis to create submission
        with patch('app.docker_executor.execute_code') as mock_docker, \
             patch('app.genai.GenerativeModel') as mock_model_class:
            
            mock_docker.return_value = {
                'stdout': 'Test output',
                'stderr': '',
                'exit_code': 0,
                'execution_time': 1.0,
                'error': None
            }
            
            mock_model = mock_model_class.return_value
            mock_response = type('MockResponse', (), {
                'text': json.dumps({
                    "errors": [],
                    "suggestions": ["Test suggestion"],
                    "optimizations": ["Test optimization"],
                    "output": "Test analysis",
                    "quality_metrics": {"summary": "Test"}
                }),
                'candidates': [type('MockCandidate', (), {'finish_reason': 1})()]
            })()
            mock_model.generate_content.return_value = mock_response
            
            analysis_response = self.session.post(
                f"{self.BASE_URL}/api/analyze",
                json={
                    "code": "print('test')",
                    "language": "python"
                }
            )
            assert analysis_response.status_code == 200
        
        # Check submissions increased
        submissions_response = self.session.get(f"{self.BASE_URL}/api/submissions")
        assert submissions_response.status_code == 200
        new_submissions = submissions_response.json()["submissions"]
        assert len(new_submissions) == initial_count + 1
        
        # Get specific submission
        if new_submissions:
            submission_id = new_submissions[0]["id"]
            submission_response = self.session.get(
                f"{self.BASE_URL}/api/submissions/{submission_id}"
            )
            assert submission_response.status_code == 200
            submission_data = submission_response.json()
            assert "code" in submission_data
            assert "analysis_result" in submission_data
            assert submission_data["language"] == "python"
    
    def test_debug_endpoints(self):
        """Test debug endpoints"""
        # Test ping
        ping_response = self.session.get(f"{self.BASE_URL}/api/debug/ping")
        assert ping_response.status_code == 200
        assert ping_response.json() == {"ok": True}
        
        # Test models endpoint (may fail if no API key)
        models_response = self.session.get(f"{self.BASE_URL}/api/debug/models")
        # Should either succeed or fail with specific error
        assert models_response.status_code in [200, 500]
    
    def test_invalid_endpoints(self):
        """Test invalid endpoints return 404"""
        response = self.session.get(f"{self.BASE_URL}/api/nonexistent")
        assert response.status_code == 404
        
        response = self.session.post(f"{self.BASE_URL}/auth/nonexistent")
        assert response.status_code == 404
    
    def test_malformed_requests(self):
        """Test malformed requests are handled properly"""
        self._authenticate()
        
        # Invalid JSON
        response = self.session.post(
            f"{self.BASE_URL}/api/analyze",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
        
        # Missing required fields
        response = self.session.post(
            f"{self.BASE_URL}/api/analyze",
            json={"code": "print('hello')"}  # Missing language
        )
        assert response.status_code == 400
    
    def _authenticate(self):
        """Helper method to authenticate test user"""
        if not self.user_token:
            # Register user
            signup_response = self.session.post(
                f"{self.BASE_URL}/auth/signup",
                json=self.test_user
            )
            if signup_response.status_code == 200:
                self.user_token = signup_response.json()["access_token"]
            else:
                # User might already exist, try login
                login_response = self.session.post(
                    f"{self.BASE_URL}/auth/login",
                    json={
                        "username": self.test_user["username"],
                        "password": self.test_user["password"]
                    }
                )
                if login_response.status_code == 200:
                    self.user_token = login_response.json()["access_token"]
        
        if self.user_token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.user_token}"
            })


class TestAPIPerformance:
    """Performance tests for API endpoints"""
    
    BASE_URL = "http://localhost:8000"
    
    def test_ping_response_time(self):
        """Test that ping endpoint responds quickly"""
        start_time = time.time()
        response = requests.get(f"{self.BASE_URL}/api/debug/ping")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second
    
    @patch('app.docker_executor.execute_code')
    @patch('app.genai.GenerativeModel')
    def test_analysis_response_time(self, mock_model_class, mock_docker_execute):
        """Test that code analysis completes within reasonable time"""
        # Setup mocks for fast response
        mock_docker_execute.return_value = {
            'stdout': 'Hello',
            'stderr': '',
            'exit_code': 0,
            'execution_time': 0.1,
            'error': None
        }
        
        mock_model = mock_model_class.return_value
        mock_response = type('MockResponse', (), {
            'text': '{"errors": [], "suggestions": [], "optimizations": [], "output": "test"}',
            'candidates': [type('MockCandidate', (), {'finish_reason': 1})()]
        })()
        mock_model.generate_content.return_value = mock_response
        
        # Create authenticated session
        session = requests.Session()
        
        # Register and authenticate
        test_user = {
            "username": f"perftest_{int(time.time())}",
            "password": "testpass123",
            "email": f"perftest_{int(time.time())}@example.com"
        }
        
        signup_response = session.post(f"{self.BASE_URL}/auth/signup", json=test_user)
        if signup_response.status_code == 200:
            token = signup_response.json()["access_token"]
            session.headers.update({"Authorization": f"Bearer {token}"})
            
            # Test analysis performance
            start_time = time.time()
            response = session.post(
                f"{self.BASE_URL}/api/analyze",
                json={
                    "code": "print('Hello, World!')",
                    "language": "python"
                }
            )
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 10.0  # Should complete within 10 seconds
