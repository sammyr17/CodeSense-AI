"""
Test configuration and fixtures
"""
import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database import Base, get_db
from main import app
from auth import create_access_token
import docker


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_docker_client():
    """Mock Docker client for testing"""
    mock_client = Mock()
    mock_container = Mock()
    mock_container.wait.return_value = {'StatusCode': 0}
    mock_container.logs.return_value = b"Hello, World!\n"
    mock_client.containers.run.return_value = mock_container
    mock_client.images.get.return_value = Mock()
    mock_client.ping.return_value = True
    return mock_client


@pytest.fixture(scope="function")
def test_db():
    """Create test database"""
    # Use in-memory SQLite for testing
    engine = create_engine(
        "sqlite:///:memory:", 
        echo=False,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session for the test
    db_session = TestingSessionLocal()
    
    def override_get_db():
        try:
            # Return the same session for consistency
            yield db_session
        except Exception:
            db_session.rollback()
            raise
        finally:
            pass  # Don't close here, we'll close after the test
    
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        yield db_session
    finally:
        # Clean up
        db_session.rollback()  # Rollback any uncommitted changes
        db_session.close()
        app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def authenticated_client(test_db):
    """Create authenticated test client"""
    # Create test user with unique username for each test
    import time
    from database import create_user
    unique_username = f"testuser_{int(time.time() * 1000000)}"
    
    user = create_user(
        db=test_db,
        username=unique_username,
        password="testpass123",
        email=f"{unique_username}@example.com",
        full_name="Test User"
    )
    
    # Commit the user to the database
    test_db.commit()
    
    # Create access token
    token = create_access_token(data={"sub": user.username})
    
    # Create client with the same database session
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client, user


@pytest.fixture
def sample_code():
    """Sample code for testing"""
    return {
        "python": 'print("Hello, World!")\nfor i in range(3):\n    print(f"Number: {i}")',
        "javascript": 'console.log("Hello, World!");\nfor(let i = 0; i < 3; i++) {\n    console.log(`Number: ${i}`);\n}',
        "java": 'public class Test {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
        "cpp": '#include <iostream>\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
        "go": 'package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Hello, World!")\n}'
    }


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response"""
    return {
        "errors": [],
        "suggestions": ["Consider adding error handling", "Use more descriptive variable names"],
        "optimizations": ["Code looks good", "Consider using list comprehension"],
        "output": "Analysis of code behavior and quality",
        "quality_metrics": {
            "summary": "Good code quality",
            "complexity_issues": [],
            "security_issues": [],
            "recommendations": ["Keep up the good work"],
            "security_analysis": "No security issues detected"
        }
    }


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up test environment variables"""
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")


@pytest.fixture
def mock_lizard_analysis():
    """Mock Lizard analysis result"""
    mock_analysis = Mock()
    mock_analysis.nloc = 10
    mock_analysis.function_list = [
        Mock(cyclomatic_complexity=2),
        Mock(cyclomatic_complexity=3)
    ]
    return mock_analysis
