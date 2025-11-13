# CodeSense AI

AI-Powered Code Analysis Platform with User Authentication and Submission History

## Project Overview

CodeSense AI is a comprehensive web application that analyzes code using Google's Gemini AI. It provides instant feedback on code quality, error detection, optimization suggestions, and expected output for multiple programming languages. The platform includes user authentication, submission history, and comprehensive logging.

## Features

- **AI-Powered Analysis**: Uses Google Gemini AI for comprehensive code analysis
- **Multi-Language Support**: Supports JavaScript, Python, Java, C++, Go, and more
- **User Authentication**: Secure JWT-based login and signup system
- **Submission History**: Automatically saves and tracks all code analysis submissions
- **Real-time Analysis**: Get instant feedback on code quality, errors, and optimizations
- **Download Reports**: Generate downloadable analysis reports
- **Modern UI**: Clean, responsive interface with React components
- **Comprehensive Logging**: Structured logging for debugging and monitoring

## Technologies Used

- **Backend**: FastAPI (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Frontend**: HTML5, CSS3, JavaScript with React components
- **AI**: Google Gemini API
- **Server**: Uvicorn (ASGI server)
- **Logging**: Python logging with file rotation

## Prerequisites

- **Python 3.10 or higher** (recommended for best compatibility)
- **PostgreSQL 12 or higher** (for database functionality)
- **Docker** (optional, for containerized PostgreSQL)
- **pip** (Python package installer)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

### 1. Setup PostgreSQL Database

#### Option A: Using Docker (Recommended)
```bash
# Run PostgreSQL in a Docker container
docker run --name codesense-postgres \
  -e POSTGRES_USER=samar \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=codesense_ai \
  -p 5432:5432 \
  -d postgres:15
```

#### Option B: Local PostgreSQL Installation
1. Install PostgreSQL on your system
2. Create a database user and database:
   ```sql
   CREATE USER samar WITH PASSWORD 'admin';
   CREATE DATABASE codesense_ai OWNER samar;
   GRANT ALL PRIVILEGES ON DATABASE codesense_ai TO samar;
   ```

### 2. Setup Python Environment

1. **Navigate to the project directory**:
   ```bash
   cd CodeSense-AI
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configure Environment Variables

1. **Copy the environment template**:
   ```bash
   copy .env.example .env  # Windows
   # or
   cp .env.example .env    # macOS/Linux
   ```

2. **Edit `.env` and configure the following**:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   DATABASE_URL=postgresql://samar:admin@localhost:5432/codesense_ai
   SECRET_KEY=your-secret-key-change-this-in-production
   PORT=8000
   ```

### 4. Initialize the Database

```bash
python setup_database.py
```

This will create the necessary database tables for user authentication and submission history.

## Running the Application

### 1. Start the PostgreSQL Database (if using Docker)
```bash
docker start codesense-postgres
```

### 2. Start the Python Server
```bash
# Make sure your virtual environment is activated
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the Application
Open your browser and navigate to:
```
http://localhost:8000
```

### 4. Create an Account
1. Click "Sign Up" to create a new account
2. Fill in your username, password, and optional details
3. Login with your credentials
4. Start analyzing code!

## Project Structure

```
.
├── main.py                 # Application entry point and server configuration
├── app.py                  # API routes for code analysis and submissions
├── auth.py                 # Authentication endpoints and JWT handling
├── database.py             # Database models and user management
├── logger_config.py        # Centralized logging configuration
├── setup_database.py       # Database initialization script
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your environment variables (create this)
├── templates/
│   └── index.html         # Main HTML page with React components
├── submissions/           # Directory for stored code files
├── logs/                  # Application logs directory
└── README.md              # This file
```

## API Endpoints

### Authentication Endpoints

#### POST `/auth/signup`
Create a new user account.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password",
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

#### POST `/auth/login`
Login with existing credentials.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }
}
```

### Code Analysis Endpoints

#### POST `/api/analyze` (Requires Authentication)
Analyzes code using AI and saves submission to user's history.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "code": "print('Hello, World!')",
  "language": "python"
}
```

**Response:**
```json
{
  "errors": [
    {
      "line": 1,
      "message": "Error description",
      "severity": "error"
    }
  ],
  "suggestions": ["Suggestion 1", "Suggestion 2"],
  "optimizations": ["Optimization 1", "Optimization 2"],
  "output": "Expected output"
}
```

### Submission History Endpoints

#### GET `/api/submissions` (Requires Authentication)
Get all submissions for the current user.

#### GET `/api/submissions/{id}` (Requires Authentication)
Get a specific submission with code and analysis results.

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `DATABASE_URL`: PostgreSQL connection string (required)
- `SECRET_KEY`: JWT secret key for authentication (required)
- `PORT`: Server port (default: 8000)

### Database Configuration

The application uses PostgreSQL with the following default connection:
- **Host**: localhost
- **Port**: 5432
- **Database**: codesense_ai
- **User**: samar
- **Password**: admin

### Logging Configuration

Logs are automatically created in the `logs/` directory:
- `codesense_ai_YYYYMMDD.log`: General application logs
- `codesense_ai_errors_YYYYMMDD.log`: Error-specific logs

## Development

### Running in Development Mode

The application runs with auto-reload enabled by default. Any changes to Python files will automatically restart the server.

### Making Changes

- **Backend**: Edit `app.py` for API logic, `auth.py` for authentication, `database.py` for models
- **Frontend**: Edit `templates/index.html` for UI components
- **Database**: Modify models in `database.py` and run migrations if needed
- **Logging**: Configure logging in `logger_config.py`

## Deployment

### Production Deployment

For production, use a production ASGI server like Gunicorn with Uvicorn workers:

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Or deploy to platforms like:
- **Heroku**: Add a `Procfile` with `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Railway**: Configure start command
- **DigitalOcean App Platform**: Set start command
- **AWS/GCP/Azure**: Use containerized deployment

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY is not configured"**
   - Make sure you've created a `.env` file with your API key
   - Verify the key is correct and has no extra spaces

2. **Database connection failed**
   - Ensure PostgreSQL is running (check Docker container or local service)
   - Verify database credentials in `.env` file
   - Run `python setup_database.py` to initialize the database

3. **Authentication errors (403/401)**
   - Make sure you're logged in before analyzing code
   - Check if JWT token has expired (tokens last 30 minutes)
   - Clear browser storage and login again

4. **Port already in use**
   - Change the `PORT` in `.env` or use a different port
   - Kill the process using the port: `netstat -ano | findstr :8000` (Windows)

5. **Module not found errors**
   - Make sure you've activated your virtual environment
   - Run `pip install -r requirements.txt` again

6. **Submission history not working**
   - Ensure database is properly initialized
   - Check that `submissions/` directory exists and is writable
   - Verify user authentication is working

### Docker Commands

```bash
# Start PostgreSQL container
docker start codesense-postgres

# Stop PostgreSQL container
docker stop codesense-postgres

# View container logs
docker logs codesense-postgres

# Connect to PostgreSQL directly
docker exec -it codesense-postgres psql -U samar -d codesense_ai
```

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the repository.
