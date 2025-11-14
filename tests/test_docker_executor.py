"""
Unit tests for docker_executor.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
from docker_executor import DockerExecutor, docker_executor


class TestDockerExecutor:
    """Test DockerExecutor class"""
    
    @patch('docker_executor.docker.from_env')
    def test_init_success(self, mock_docker):
        """Test successful Docker client initialization"""
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.return_value = mock_client
        
        executor = DockerExecutor()
        
        assert executor.client == mock_client
        assert executor.is_available() is True
        mock_client.ping.assert_called_once()
    
    @patch('docker_executor.docker.from_env')
    def test_init_failure(self, mock_docker):
        """Test failed Docker client initialization"""
        mock_docker.side_effect = Exception("Docker not available")
        
        executor = DockerExecutor()
        
        assert executor.client is None
        assert executor.is_available() is False
    
    def test_get_docker_image(self):
        """Test getting Docker images for different languages"""
        executor = DockerExecutor()
        
        assert executor.get_docker_image('python') == 'python:3.11-slim'
        assert executor.get_docker_image('javascript') == 'node:22-alpine'
        assert executor.get_docker_image('java') == 'openjdk:22-jre-slim'
        assert executor.get_docker_image('cpp') == 'gcc:latest'
        assert executor.get_docker_image('go') == 'golang:1.22-alpine'
        assert executor.get_docker_image('unknown') == 'ubuntu:20.04'
    
    def test_get_file_extension(self):
        """Test getting file extensions for different languages"""
        executor = DockerExecutor()
        
        assert executor.get_file_extension('python') == '.py'
        assert executor.get_file_extension('javascript') == '.js'
        assert executor.get_file_extension('java') == '.java'
        assert executor.get_file_extension('cpp') == '.cpp'
        assert executor.get_file_extension('go') == '.go'
        assert executor.get_file_extension('unknown') == '.txt'
    
    def test_get_run_command(self):
        """Test getting run commands for different languages"""
        executor = DockerExecutor()
        
        assert executor.get_run_command('python', 'test.py') == ['python', 'test.py']
        assert executor.get_run_command('javascript', 'test.js') == ['node', 'test.js']
        assert 'javac' in ' '.join(executor.get_run_command('java', 'Test.java'))
        assert 'g++' in ' '.join(executor.get_run_command('cpp', 'test.cpp'))
        assert 'GOCACHE' in ' '.join(executor.get_run_command('go', 'test.go'))
        assert executor.get_run_command('unknown', 'test.txt') == ['cat', 'test.txt']
    
    @patch('docker_executor.docker.from_env')
    def test_execute_code_docker_unavailable(self, mock_docker):
        """Test code execution when Docker is unavailable"""
        mock_docker.side_effect = Exception("Docker not available")
        executor = DockerExecutor()
        
        result = executor.execute_code("print('hello')", "python")
        
        assert result['exit_code'] == 1
        assert result['error'] == 'Docker not available'
        assert 'Docker is not available' in result['stderr']
    
    @patch('docker_executor.docker.from_env')
    def test_execute_code_success(self, mock_docker):
        """Test successful code execution"""
        # Setup mock Docker client
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.return_value = mock_client
        
        # Setup mock container
        mock_container = Mock()
        mock_container.wait.return_value = {'StatusCode': 0}
        mock_container.logs.return_value = b"Hello, World!\n"
        mock_client.containers.run.return_value = mock_container
        
        # Setup mock image
        mock_client.images.get.return_value = Mock()
        
        executor = DockerExecutor()
        result = executor.execute_code("print('Hello, World!')", "python")
        
        assert result['exit_code'] == 0
        assert result['stdout'] == "Hello, World!"
        assert result['stderr'] == ""
        assert result['error'] is None
        assert result['execution_time'] >= 0
    
    @patch('docker_executor.docker.from_env')
    def test_execute_code_failure(self, mock_docker):
        """Test code execution failure"""
        # Setup mock Docker client
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.return_value = mock_client
        
        # Setup mock container with error
        mock_container = Mock()
        mock_container.wait.return_value = {'StatusCode': 1}
        mock_container.logs.return_value = b"SyntaxError: invalid syntax\n"
        mock_client.containers.run.return_value = mock_container
        
        # Setup mock image
        mock_client.images.get.return_value = Mock()
        
        executor = DockerExecutor()
        result = executor.execute_code("print('Hello World'", "python")  # Missing closing quote
        
        assert result['exit_code'] == 1
        assert result['stdout'] == ""
        assert "SyntaxError" in result['stderr']
        assert result['error'] == 'Execution failed'
    
    @patch('docker_executor.docker.from_env')
    def test_execute_code_timeout(self, mock_docker):
        """Test code execution timeout"""
        # Setup mock Docker client
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.return_value = mock_client
        
        # Setup mock container that times out
        mock_container = Mock()
        mock_container.wait.side_effect = Exception("Timeout")
        mock_client.containers.run.return_value = mock_container
        
        # Setup mock image
        mock_client.images.get.return_value = Mock()
        
        executor = DockerExecutor()
        result = executor.execute_code("while True: pass", "python", timeout=1)
        
        assert result['exit_code'] == 124  # Timeout exit code
        assert 'timeout' in result['stderr'].lower()
        assert result['error'] == 'Timeout or container error'
    
    @patch('docker_executor.docker.from_env')
    def test_execute_code_image_not_found(self, mock_docker):
        """Test code execution when Docker image is not found"""
        # Setup mock Docker client
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.return_value = mock_client
        
        # Setup image not found error
        from docker.errors import ImageNotFound
        mock_client.images.get.side_effect = ImageNotFound("Image not found")
        mock_client.images.pull.side_effect = ImageNotFound("Cannot pull image")
        
        executor = DockerExecutor()
        result = executor.execute_code("print('hello')", "python")
        
        assert result['exit_code'] == 1
        assert result['error'] == 'Image not found'
        assert 'not available' in result['stderr']
    
    @patch('docker_executor.docker.from_env')
    def test_cleanup(self, mock_docker):
        """Test Docker cleanup"""
        # Setup mock Docker client
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.return_value = mock_client
        
        # Setup mock containers
        mock_container1 = Mock()
        mock_container1.name = "codesense_test_1"
        mock_container2 = Mock()
        mock_container2.name = "other_container"
        
        mock_client.containers.list.return_value = [mock_container1, mock_container2]
        
        executor = DockerExecutor()
        executor.cleanup()
        
        # Should only remove containers with 'codesense' in name
        mock_container1.remove.assert_called_once()
        mock_container2.remove.assert_not_called()


class TestGlobalExecutorInstance:
    """Test the global docker_executor instance"""
    
    def test_global_instance_exists(self):
        """Test that global docker_executor instance exists"""
        assert docker_executor is not None
        assert isinstance(docker_executor, DockerExecutor)
    
    @patch('docker_executor.docker.from_env')
    def test_global_instance_methods(self, mock_docker):
        """Test that global instance methods work"""
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.return_value = mock_client
        
        # Test method calls on global instance
        assert docker_executor.get_docker_image('python') == 'python:3.11-slim'
        assert docker_executor.get_file_extension('python') == '.py'
