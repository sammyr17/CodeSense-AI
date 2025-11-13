# Docker Code Execution Setup

This document explains the Docker integration for secure code execution in CodeSense AI.

## Overview

CodeSense AI now executes user code in isolated Docker containers to:
- Capture actual stdout and stderr output
- Provide secure sandboxed execution
- Only send code to Gemini AI if execution is successful

## Prerequisites

1. **Docker Desktop** must be installed and running
2. **Python Docker SDK** must be installed: `pip install docker`

## How It Works

1. When a code analysis request comes in, the code is first executed in a Docker container
2. The execution captures:
   - Standard output (stdout)
   - Standard error (stderr) 
   - Exit code
   - Execution time
3. If execution is successful (exit code 0), the code and output are sent to Gemini for analysis
4. If execution fails, only the execution error is returned (Gemini analysis is skipped)

## Supported Languages

- **Python**: Uses `python:3.9-slim` image
- **JavaScript**: Uses `node:18-alpine` image  
- **Java**: Uses `openjdk:11-jre-slim` image
- **C++**: Uses `gcc:latest` image
- **C**: Uses `gcc:latest` image
- **Go**: Uses `golang:1.19-alpine` image

## Security Features

- **Memory limit**: 128MB per container
- **CPU limit**: 50% CPU usage
- **Network disabled**: No internet access
- **Non-root user**: Runs as `nobody` user
- **Timeout**: 30 second execution limit
- **Auto-cleanup**: Containers are automatically removed

## Installation

1. Install Docker dependencies:
   ```bash
   pip install -r requirements_docker.txt
   ```

2. Ensure Docker Desktop is running

3. The system will automatically pull required Docker images on first use

## Configuration

The Docker executor is automatically initialized when the application starts. No additional configuration is required.

## Error Handling

If Docker is not available:
- The system will log an error
- Code execution will fail gracefully
- Users will see a "Docker not available" message

## Troubleshooting

1. **Docker not found**: Ensure Docker Desktop is installed and running
2. **Permission errors**: Ensure your user has Docker permissions
3. **Image pull failures**: Check internet connection for initial image downloads
4. **Timeout errors**: Code taking longer than 30 seconds will be terminated

## Frontend Changes

The UI now displays two separate sections:
- **Code Execution Output**: Shows actual stdout/stderr from Docker execution
- **AI Analysis**: Shows Gemini's code quality analysis (only if execution succeeds)

Success/failure indicators are shown with color-coded badges.
