# CodeSense AI - Test Environment Specifications

## 🖥️ **Hardware Requirements**

### **Minimum Requirements**
| Component | Specification | Reason |
|-----------|---------------|---------|
| **CPU** | 2 cores, 2.0 GHz | Docker container execution |
| **RAM** | 4 GB | Multiple containers + database |
| **Storage** | 10 GB free space | Docker images + test data |
| **Network** | Broadband internet | Docker image downloads |

### **Recommended Requirements**
| Component | Specification | Reason |
|-----------|---------------|---------|
| **CPU** | 4+ cores, 3.0+ GHz | Faster test execution |
| **RAM** | 8+ GB | Parallel test execution |
| **Storage** | 20+ GB SSD | Faster I/O operations |
| **Network** | High-speed internet | Quick image pulls |

### **Performance Considerations**
- **Docker Overhead**: Each test container uses ~50-100MB RAM
- **Database**: PostgreSQL requires ~100MB RAM minimum
- **Concurrent Tests**: Each parallel test adds ~200MB RAM usage
- **Build Cache**: Docker images can use 2-5GB storage

## 💻 **Software Requirements**

### **Core Dependencies**
| Software | Version | Purpose | Installation |
|----------|---------|---------|-------------|
| **Python** | 3.8+ | Runtime environment | `python --version` |
| **Docker** | 20.0+ | Container execution | `docker --version` |
| **PostgreSQL** | 12+ | Database (production) | `psql --version` |
| **Git** | 2.0+ | Version control | `git --version` |

### **Python Dependencies**
```bash
# Core application
pip install -r requirements.txt

# Testing dependencies
pip install -r requirements-test.txt
```

### **Docker Images Required**
| Language | Image | Size | Purpose |
|----------|-------|------|---------|
| Python | `python:3.11-slim` | ~150MB | Python code execution |
| JavaScript | `node:22-alpine` | ~120MB | Node.js execution |
| Java | `openjdk:22-jre-slim` | ~200MB | Java compilation/execution |
| C++ | `gcc:latest` | ~300MB | C++ compilation |
| Go | `golang:1.22-alpine` | ~400MB | Go compilation/execution |

## 🏗️ **Environment Setup**

### **1. Development Environment**
```bash
# Clone repository
git clone <repository-url>
cd CodeSense-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configurations
```

### **2. Database Setup**
```bash
# Option 1: PostgreSQL (Production-like)
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres createdb codesense_ai_test
sudo -u postgres createuser testuser --pwprompt

# Option 2: SQLite (Testing only - automatic)
# Tests use in-memory SQLite by default
```

### **3. Docker Setup**
```bash
# Install Docker Desktop or Docker Engine
# Verify installation
docker --version
docker run hello-world

# Pull required images (optional - auto-pulled during tests)
docker pull python:3.11-slim
docker pull node:22-alpine
docker pull openjdk:22-jre-slim
docker pull gcc:latest
docker pull golang:1.22-alpine
```

## 🧪 **Test Environment Configurations**

### **Test Database Configuration**
```python
# tests/conftest.py
TEST_DATABASE_URL = "sqlite:///:memory:"  # Fast, isolated
# OR for PostgreSQL testing:
# TEST_DATABASE_URL = "postgresql://testuser:testpass@localhost:5432/codesense_test"
```

### **Environment Variables for Testing**
```bash
# .env.test
SECRET_KEY=test-secret-key-change-in-production
GEMINI_API_KEY=test-gemini-key-or-mock
DATABASE_URL=sqlite:///:memory:
DOCKER_HOST=unix:///var/run/docker.sock
LOG_LEVEL=DEBUG
```

### **Docker Test Configuration**
```python
# Container limits for testing
MEMORY_LIMIT = "128m"
CPU_QUOTA = 50000  # 50% of one core
NETWORK_DISABLED = True
EXECUTION_TIMEOUT = 15  # seconds
```

## 🔧 **CI/CD Environment**

### **GitHub Actions Configuration**
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

### **Docker-in-Docker for CI**
```yaml
# For CI environments that need Docker
services:
  docker:
    image: docker:dind
    privileged: true
```

## 📊 **Performance Benchmarks**

### **Expected Test Performance**
| Test Category | Count | Duration | Memory |
|---------------|-------|----------|---------|
| Unit Tests | ~50 tests | <30 seconds | <500MB |
| Integration Tests | ~15 tests | <60 seconds | <1GB |
| Docker Tests | ~20 tests | <120 seconds | <2GB |
| **Total** | **~85 tests** | **<3 minutes** | **<2GB** |

### **Performance Monitoring**
```bash
# Monitor test performance
pytest --durations=10  # Show 10 slowest tests
pytest --benchmark-only  # Run only benchmark tests

# Monitor resource usage
docker stats  # During Docker tests
htop  # System resource monitoring
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Docker Permission Errors**
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again

# Windows: Ensure Docker Desktop is running
# Mac: Ensure Docker Desktop has proper permissions
```

#### **Port Conflicts**
```bash
# Check for port usage
netstat -tulpn | grep :8000
lsof -i :8000

# Kill conflicting processes
kill -9 <PID>
```

#### **Database Connection Issues**
```bash
# PostgreSQL not running
sudo systemctl start postgresql
brew services start postgresql  # Mac

# Connection refused
# Check DATABASE_URL in .env
# Verify credentials and database exists
```

#### **Memory Issues**
```bash
# Increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory

# Clean up Docker resources
docker system prune -a
docker volume prune
```

### **Test Debugging**
```bash
# Run specific test with verbose output
pytest tests/test_database.py::TestUserModel::test_user_creation -v -s

# Run with debugger
pytest --pdb tests/test_app.py

# Run with coverage and HTML report
pytest --cov=. --cov-report=html tests/

# Skip slow tests
pytest -m "not slow" tests/
```

## 📋 **Environment Validation Checklist**

### **Pre-Test Validation**
- [ ] Python 3.8+ installed and accessible
- [ ] Docker daemon running and accessible
- [ ] Required Docker images available or internet access for pulling
- [ ] Database accessible (PostgreSQL or SQLite)
- [ ] All Python dependencies installed
- [ ] Environment variables configured
- [ ] Sufficient disk space (10GB+)
- [ ] Sufficient RAM (4GB+)

### **Test Execution Validation**
- [ ] All unit tests pass
- [ ] Integration tests pass (with running server)
- [ ] Coverage meets minimum threshold (80%)
- [ ] No test warnings or deprecation notices
- [ ] Performance tests within acceptable limits
- [ ] Docker containers clean up properly
- [ ] No resource leaks detected

### **Post-Test Cleanup**
- [ ] Docker containers removed
- [ ] Temporary files cleaned
- [ ] Test database reset
- [ ] Coverage reports generated
- [ ] Test artifacts archived
