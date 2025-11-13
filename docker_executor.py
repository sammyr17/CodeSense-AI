"""
Docker Code Execution Module
Executes code in isolated Docker containers and captures stdout/stderr
"""
import docker
import tempfile
import os
import json
import time
from typing import Dict, Tuple, Optional
from logger_config import setup_logging

logger = setup_logging(__name__)

class DockerExecutor:
    """Handles code execution in Docker containers"""
    
    def __init__(self):
        """Initialize Docker client"""
        try:
            self.client = docker.from_env()
            # Test Docker connection
            self.client.ping()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Docker is available"""
        return self.client is not None
    
    def get_docker_image(self, language: str) -> str:
        """Get appropriate Docker image for the language"""
        images = {
            'python': 'python:3.11-slim',
            'javascript': 'node:22-alpine',
            'java': 'openjdk:22-jre-slim',
            'cpp': 'gcc:latest',
            'go': 'golang:1.22-alpine'
        }
        return images.get(language, 'ubuntu:20.04')
    
    def get_file_extension(self, language: str) -> str:
        """Get file extension for the language"""
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java',
            'cpp': '.cpp',
            'go': '.go'
        }
        return extensions.get(language, '.txt')
    
    def get_run_command(self, language: str, filename: str) -> list:
        """Get command to run the code file"""
        commands = {
            'python': ['python', filename],
            'javascript': ['node', filename],
            'java': ['sh', '-c', f'javac {filename} && java {filename.replace(".java", "")}'],
            'cpp': ['sh', '-c', f'g++ -std=c++17 -o program {filename} && ./program'],
            'go': ['sh', '-c', f'cd /workspace && GOCACHE=/tmp GOPROXY=direct GOSUMDB=off GO111MODULE=auto go run {filename}']
        }
        return commands.get(language, ['cat', filename])
    
    def execute_code(self, code: str, language: str, timeout: int = 15) -> Dict:
        """
        Execute code in a Docker container
        
        Args:
            code: The code to execute
            language: Programming language
            timeout: Execution timeout in seconds
            
        Returns:
            Dict with stdout, stderr, exit_code, and execution_time
        """
        if not self.is_available():
            return {
                'stdout': '',
                'stderr': 'Docker is not available',
                'exit_code': 1,
                'execution_time': 0,
                'error': 'Docker not available'
            }
        
        try:
            # Get Docker image and file extension
            image = self.get_docker_image(language)
            extension = self.get_file_extension(language)
            filename = f'code{extension}'
            
            # Create temporary directory for code file
            with tempfile.TemporaryDirectory() as temp_dir:
                # Write code to file
                code_file_path = os.path.join(temp_dir, filename)
                with open(code_file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                # Get run command
                run_command = self.get_run_command(language, filename)
                
                logger.info(f"Executing {language} code in Docker container with image: {image}")
                start_time = time.time()
                
                try:
                    # Pull image if not available
                    try:
                        self.client.images.get(image)
                    except docker.errors.ImageNotFound:
                        logger.info(f"Pulling Docker image: {image}")
                        self.client.images.pull(image)
                    
                    # Run container
                    # Enable network for Go temporarily to avoid module issues
                    network_disabled = language != 'go'
                    container = self.client.containers.run(
                        image=image,
                        command=run_command,
                        volumes={temp_dir: {'bind': '/workspace', 'mode': 'rw'}},
                        working_dir='/workspace',
                        detach=True,
                        remove=True,
                        mem_limit='128m',  # Limit memory usage
                        cpu_period=100000,  # CPU limit
                        cpu_quota=50000,    # 50% CPU
                        network_disabled=network_disabled,  # Enable network for Go
                        user='nobody'  # Run as non-root user
                    )
                    
                    # Wait for container to finish with shorter timeout
                    try:
                        result = container.wait(timeout=timeout)
                        exit_code = result['StatusCode']
                        logger.info(f"Container finished with exit code: {exit_code}")
                    except Exception as e:
                        logger.warning(f"Container execution timeout or error: {e}")
                        try:
                            container.kill()
                            logger.info("Container killed due to timeout")
                        except Exception as kill_error:
                            logger.warning(f"Failed to kill container: {kill_error}")
                        return {
                            'stdout': '',
                            'stderr': f'Execution timeout ({timeout}s) or container error: {str(e)}',
                            'exit_code': 124,  # Timeout exit code
                            'execution_time': timeout,
                            'error': 'Timeout or container error'
                        }
                    
                    # Get logs
                    logs = container.logs(stdout=True, stderr=True).decode('utf-8', errors='replace')
                    
                    # Split stdout and stderr (Docker combines them)
                    # For simplicity, we'll treat all output as stdout unless there's an error
                    if exit_code == 0:
                        stdout = logs
                        stderr = ''
                    else:
                        stdout = ''
                        stderr = logs
                    
                    execution_time = time.time() - start_time
                    
                    logger.info(f"Code execution completed in {execution_time:.2f}s with exit code: {exit_code}")
                    
                    return {
                        'stdout': stdout.strip(),
                        'stderr': stderr.strip(),
                        'exit_code': exit_code,
                        'execution_time': execution_time,
                        'error': None if exit_code == 0 else 'Execution failed'
                    }
                    
                except docker.errors.ContainerError as e:
                    execution_time = time.time() - start_time
                    logger.warning(f"Container execution failed: {e}")
                    return {
                        'stdout': '',
                        'stderr': str(e),
                        'exit_code': e.exit_status,
                        'execution_time': execution_time,
                        'error': 'Container execution failed'
                    }
                except docker.errors.ImageNotFound as e:
                    logger.error(f"Docker image not found: {e}")
                    return {
                        'stdout': '',
                        'stderr': f'Docker image not available: {image}',
                        'exit_code': 1,
                        'execution_time': 0,
                        'error': 'Image not found'
                    }
                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(f"Docker execution error: {e}")
                    return {
                        'stdout': '',
                        'stderr': f'Docker execution error: {str(e)}',
                        'exit_code': 1,
                        'execution_time': execution_time,
                        'error': 'Docker execution error'
                    }
        
        except Exception as e:
            logger.error(f"Failed to execute code in Docker: {e}")
            return {
                'stdout': '',
                'stderr': f'Failed to execute code: {str(e)}',
                'exit_code': 1,
                'execution_time': 0,
                'error': 'Execution setup failed'
            }
    
    def cleanup(self):
        """Cleanup Docker resources"""
        if self.client:
            try:
                # Remove any dangling containers
                containers = self.client.containers.list(all=True, filters={'status': 'exited'})
                for container in containers:
                    if 'codesense' in container.name:
                        container.remove()
                logger.info("Docker cleanup completed")
            except Exception as e:
                logger.warning(f"Docker cleanup warning: {e}")

# Global executor instance
docker_executor = DockerExecutor()
