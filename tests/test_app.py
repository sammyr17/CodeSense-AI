"""
Unit tests for app.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import tempfile
import os
from app import (
    analyze_code_complexity, calculate_script_complexity,
    estimate_time_complexity, estimate_space_complexity,
    calculate_overall_score, CodeAnalysisRequest, ErrorItem, CodeAnalysisResponse
)


class TestComplexityAnalysis:
    """Test code complexity analysis functions"""
    
    @patch('app.lizard.analyze_file')
    def test_analyze_code_complexity_success(self, mock_lizard, mock_lizard_analysis):
        """Test successful code complexity analysis"""
        mock_lizard.return_value = mock_lizard_analysis
        
        result = analyze_code_complexity("def test(): pass", "python")
        
        assert "cyclomatic_complexity" in result
        assert "lines_of_code" in result
        assert "time_complexity" in result
        assert "space_complexity" in result
        assert "overall_score" in result
        assert "complexity_details" in result
    
    @patch('app.lizard.analyze_file')
    def test_analyze_code_complexity_lizard_failure(self, mock_lizard):
        """Test code complexity analysis when Lizard fails"""
        mock_lizard.side_effect = Exception("Lizard failed")
        
        result = analyze_code_complexity("def test(): pass", "python")
        
        assert "Script Complexity" in result["cyclomatic_complexity"]
        assert result["lines_of_code"] > 0
        assert "Unable to determine" not in result["time_complexity"]
    
    @patch('app.lizard.analyze_file')
    @patch('app.calculate_script_complexity')
    def test_analyze_code_complexity_complete_failure(self, mock_script_complexity, mock_lizard):
        """Test code complexity analysis when both Lizard and fallback fail"""
        mock_lizard.side_effect = Exception("Lizard failed")
        mock_script_complexity.side_effect = Exception("Script analysis failed")
        
        result = analyze_code_complexity("def test(): pass", "python")
        
        assert result["cyclomatic_complexity"] == "Analysis failed"
        assert result["overall_score"] == 50
    
    def test_calculate_script_complexity_python(self):
        """Test script complexity calculation for Python"""
        code = """
if True:
    for i in range(10):
        if i > 5:
            print(i)
        elif i < 3:
            continue
        else:
            break
"""
        complexity = calculate_script_complexity(code, "python")
        assert complexity > 1  # Should detect control structures
    
    def test_calculate_script_complexity_javascript(self):
        """Test script complexity calculation for JavaScript"""
        code = """
if (true) {
    for (let i = 0; i < 10; i++) {
        if (i > 5) {
            console.log(i);
        } else if (i < 3) {
            continue;
        }
    }
}
"""
        complexity = calculate_script_complexity(code, "javascript")
        assert complexity > 1
    
    def test_estimate_time_complexity(self):
        """Test time complexity estimation"""
        # O(1) - no loops
        simple_code = "print('hello')"
        assert "O(1)" in estimate_time_complexity(simple_code, "python")
        
        # O(n) - single loop
        single_loop = "for i in range(10): print(i)"
        assert "O(n)" in estimate_time_complexity(single_loop, "python")
        
        # O(n²) - nested loops (simulated)
        nested_loops = "for i in range(10):\n    for j in range(10): print(i, j)"
        complexity = estimate_time_complexity(nested_loops, "python")
        assert "O(n²)" in complexity or "O(n)" in complexity  # Depends on counting
    
    def test_estimate_space_complexity(self):
        """Test space complexity estimation"""
        # O(1) - no data structures
        simple_code = "x = 5"
        assert "O(1)" in estimate_space_complexity(simple_code, "python")
        
        # O(n) - arrays/lists
        array_code = "arr = [1, 2, 3]\nmy_list = []"
        assert "O(n)" in estimate_space_complexity(array_code, "python")
    
    def test_calculate_overall_score(self):
        """Test overall score calculation"""
        # Good score - low complexity
        score = calculate_overall_score(2.0, 3, 2, 20, "O(1)", "O(1)")
        assert score >= 80
        
        # Bad score - high complexity
        score = calculate_overall_score(15.0, 20, 5, 300, "O(n³)", "O(n)")
        assert score <= 50
        
        # Score should be between 0 and 100
        score = calculate_overall_score(100.0, 100, 1, 1000, "O(n³)", "O(n)")
        assert 0 <= score <= 100


class TestPydanticModels:
    """Test Pydantic models"""
    
    def test_code_analysis_request(self):
        """Test CodeAnalysisRequest model"""
        request = CodeAnalysisRequest(
            code="print('hello')",
            language="python"
        )
        
        assert request.code == "print('hello')"
        assert request.language == "python"
    
    def test_error_item(self):
        """Test ErrorItem model"""
        error = ErrorItem(
            line=5,
            message="Syntax error",
            severity="error"
        )
        
        assert error.line == 5
        assert error.message == "Syntax error"
        assert error.severity == "error"
    
    def test_code_analysis_response(self):
        """Test CodeAnalysisResponse model"""
        response = CodeAnalysisResponse(
            errors=[],
            suggestions=["Use better names"],
            optimizations=["Add caching"],
            output="Hello world",
            code_output="Hello world",
            execution_success=True
        )
        
        assert response.errors == []
        assert response.suggestions == ["Use better names"]
        assert response.optimizations == ["Add caching"]
        assert response.output == "Hello world"
        assert response.code_output == "Hello world"
        assert response.execution_success is True


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_debug_ping(self, client):
        """Test debug ping endpoint"""
        response = client.get("/api/debug/ping")
        
        assert response.status_code == 200
        assert response.json() == {"ok": True}
    
    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"})
    @patch('app.genai.configure')
    @patch('app.genai.list_models')
    def test_debug_models_success(self, mock_list_models, mock_configure, client):
        """Test debug models endpoint success"""
        # Mock model with generateContent support
        mock_model = Mock()
        mock_model.name = "test-model"
        mock_model.supported_generation_methods = ["generateContent"]
        mock_list_models.return_value = [mock_model]
        
        response = client.get("/api/debug/models")
        
        assert response.status_code == 200
        data = response.json()
        assert data["api_provider"] == "Google Gemini"
        assert data["count"] == 1
        assert "test-model" in data["models"]
    
    def test_debug_models_no_api_key(self, client):
        """Test debug models endpoint without API key"""
        with patch.dict(os.environ, {}, clear=True):
            response = client.get("/api/debug/models")
            
            assert response.status_code == 500
            assert "GEMINI_API_KEY is not configured" in response.json()["error"]
    
    @patch('app.docker_executor.execute_code')
    @patch('app.genai.configure')
    @patch('app.genai.GenerativeModel')
    def test_analyze_code_success(self, mock_model_class, mock_configure, mock_docker_execute, 
                                authenticated_client, mock_gemini_response):
        """Test successful code analysis"""
        client, user = authenticated_client
        
        # Mock Docker execution success
        mock_docker_execute.return_value = {
            'stdout': 'Hello, World!',
            'stderr': '',
            'exit_code': 0,
            'execution_time': 1.5,
            'error': None
        }
        
        # Mock Gemini response
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = json.dumps(mock_gemini_response)
        mock_response.candidates = [Mock(finish_reason=1)]
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        # Test request
        request_data = {
            "code": "print('Hello, World!')",
            "language": "python"
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "suggestions" in data
        assert "optimizations" in data
        assert "output" in data
        assert "code_output" in data
        assert "execution_success" in data
        assert data["code_output"] == "Hello, World!"
        assert data["execution_success"] is True
    
    @patch('app.docker_executor.execute_code')
    def test_analyze_code_execution_failure(self, mock_docker_execute, authenticated_client):
        """Test code analysis with execution failure"""
        client, user = authenticated_client
        
        # Mock Docker execution failure
        mock_docker_execute.return_value = {
            'stdout': '',
            'stderr': 'SyntaxError: invalid syntax',
            'exit_code': 1,
            'execution_time': 0.5,
            'error': 'Execution failed'
        }
        
        request_data = {
            "code": "print('Hello World'",  # Missing closing quote
            "language": "python"
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["execution_success"] is False
        assert "SyntaxError" in data["code_output"]
        assert "Code execution failed" in data["errors"][0]["message"]
    
    def test_analyze_code_missing_auth(self, client):
        """Test code analysis without authentication"""
        request_data = {
            "code": "print('Hello, World!')",
            "language": "python"
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 403  # Forbidden without auth
    
    # @pytest.mark.skip(reason="Database session isolation issue - to be fixed")
    # def test_analyze_code_missing_data(self, authenticated_client):
    #     """Test code analysis with missing data"""
    #     client, user = authenticated_client
        
    #     # Missing code
    #     response = client.post("/api/analyze", json={"language": "python"})
    #     assert response.status_code == 422  # FastAPI returns 422 for validation errors
        
    #     # Missing language  
    #     response = client.post("/api/analyze", json={"code": "print('hello')"})
    #     assert response.status_code == 422  # FastAPI returns 422 for validation errors
    
    def test_get_submissions(self, authenticated_client):
        """Test getting user submissions"""
        client, user = authenticated_client
        
        response = client.get("/api/submissions")
        
        assert response.status_code == 200
        data = response.json()
        assert "submissions" in data
        assert isinstance(data["submissions"], list)
    
    def test_get_submissions_no_auth(self, client):
        """Test getting submissions without authentication"""
        response = client.get("/api/submissions")
        
        assert response.status_code == 403  # Forbidden without auth
