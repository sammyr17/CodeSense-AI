# CodeSense AI

An AI-powered code analysis platform that provides intelligent code review, optimization suggestions, complexity analysis, and multi-language support using Google Gemini AI and Lizard complexity analyzer.

## 🚀 Features

### 🔍 Advanced Code Analysis
- **Multi-language Support**: JavaScript, Python, Java, C++, Go, C
- **AI-Powered Analysis**: Google Gemini AI for intelligent code review and suggestions
- **Accurate Cyclomatic Complexity**: Lizard library integration for precise complexity measurement
- **Script-Level Analysis**: Handles both function-based and script-level code complexity
- **Time & Space Complexity**: Algorithm complexity estimation with Big O notation
- **Overall Quality Score**: Comprehensive scoring system (0-100) based on multiple metrics
- **Security Analysis**: Identifies potential security vulnerabilities and issues
- **Code Output Prediction**: Predicts program output including loops and calculations

### 🎨 Modern User Interface
- **Real-time Code Editor**: Monaco Editor with syntax highlighting and themes
- **Collapsible Analysis Sections**: Organized, expandable results for better UX
- **Coffee-Themed Design**: Warm, professional UI with workspace imagery
- **Floating Login Panel**: Clean authentication interface with backdrop blur
- **Responsive Design**: Mobile-friendly layout and components
- **Interactive Dashboard**: User-friendly analysis interface with visual indicators
- **Report Generation**: Download comprehensive analysis reports in text format

### 👤 User Management
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Analysis History**: Track and review past code submissions with timestamps
- **Personal Dashboard**: User-specific analysis tracking and submission management
- **Session Management**: Persistent login with secure token handling

### 📊 Quality Metrics System

CodeSense AI provides comprehensive code quality analysis including:

#### Core Metrics
- **Cyclomatic Complexity**: 
  - Function-level analysis using Lizard library
  - Script-level complexity for non-function code
  - Handles nested loops, conditionals, and control flow
- **Time Complexity**: Algorithmic time complexity estimation
  - O(1) - Constant time operations
  - O(n) - Single loop operations
  - O(n²) - Nested loops
  - O(n³) or higher - Multiple nested loops
- **Space Complexity**: Memory usage complexity analysis
  - O(1) - Constant space
  - O(n) - Linear space usage
  - O(log n) to O(n) - Recursive stack space
- **Lines of Code**: Accurate code size metrics from Lizard
- **Overall Score**: Composite quality score based on all metrics

#### Scoring Algorithm
The overall score (0-100) is calculated using:
- **Base Score**: 100 points
- **Complexity Penalties**: -5 to -30 points based on cyclomatic complexity
- **Function Complexity**: -5 to -25 points for high maximum complexity
- **Code Length**: -5 to -15 points for overly long code
- **Time Complexity**: -5 to -20 points for inefficient algorithms
- **Good Practice Bonuses**: +5 to +10 points for clean, simple code

#### Quality Levels
- **80-100**: 🟢 Excellent code quality
- **60-79**: 🟡 Good code quality  
- **0-59**: 🔴 Needs improvement

### 🛡️ Security & Error Handling
- **Robust API Error Handling**: Handles Gemini AI safety filters and blocked responses
- **Fallback Analysis**: Script-level complexity calculation when Lizard fails
- **Input Validation**: Secure code input processing and sanitization
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## 🛠️ Tech Stack

### Backend
- **FastAPI 0.104.1**: Modern, fast web framework for building APIs
- **Python 3.8+**: Core programming language
- **Google Gemini AI**: Advanced AI for code analysis and suggestions
- **Lizard 1.19.0**: Cyclomatic complexity analyzer for multiple languages
- **SQLAlchemy 2.0.23**: Database ORM for user and submission management
- **SQLite**: Lightweight database for development and production
- **JWT Authentication**: Secure token-based authentication
- **bcrypt**: Password hashing for security

### Frontend
- **React 18**: Modern JavaScript library for UI
- **Monaco Editor**: VS Code-powered code editor with syntax highlighting
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Babel**: JavaScript transpiler for JSX support
- **Responsive Design**: Mobile-first approach with modern CSS

### Development Tools
- **Uvicorn**: ASGI server for FastAPI
- **Python Virtual Environment**: Isolated dependency management
- **Hot Reload**: Development server with automatic reloading

## 📋 Requirements

- **Python 3.8 or higher** (Python 3.10+ recommended)
- **pip** (Python package installer)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CodeSense-AI
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
# Required: Google Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Required: JWT Secret Key (generate a secure random string)
SECRET_KEY=your_secure_secret_key_here

# Optional: Database URL (defaults to SQLite)
DATABASE_URL=sqlite:///./codesense.db

# Optional: Server Configuration
HOST=localhost
PORT=8000
```

### 5. Initialize Database
The application will automatically create the SQLite database and tables on first run.

### 6. Run the Application
```bash
python main.py
```

### 7. Access the Application
Open your browser and navigate to: `http://localhost:8000`

## 🎯 Usage Guide

### Getting Started
1. **Sign Up**: Create a new account or log in with existing credentials
2. **Write Code**: Use the Monaco editor to write or paste your code
3. **Select Language**: Choose from JavaScript, Python, Java, C++, Go, or C
4. **Analyze**: Click "Analyze Code" to get comprehensive analysis
5. **Review Results**: Expand different sections to view detailed metrics
6. **Download Report**: Get a complete analysis report in text format

### Analysis Sections
- **📊 Quality Metrics**: Comprehensive code quality analysis (displayed first)
- **⚠️ Issues Found**: Syntax errors, warnings, and code issues
- **💡 Suggestions**: AI-generated improvement recommendations  
- **⚡ Optimizations**: Performance and best practice suggestions
- **📄 Code Output**: Predicted program execution results

### Quality Metrics Details
- **Overall Score**: Your code's quality rating out of 100
- **Cyclomatic Complexity**: Measure of code's logical complexity
- **Time Complexity**: Algorithm efficiency in Big O notation
- **Space Complexity**: Memory usage complexity
- **Lines of Code**: Total executable lines
- **Security Analysis**: Potential security vulnerabilities

## 🔧 API Endpoints

### Authentication Endpoints
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - User authentication
- `GET /auth/me` - Get current user information
- `POST /auth/logout` - User logout

### Code Analysis Endpoints
- `POST /api/analyze` - Analyze code with comprehensive metrics
  ```json
  {
    "code": "your_code_here",
    "language": "python"
  }
  ```
- `GET /api/submissions` - Get user's analysis history
- `GET /api/submissions/{id}` - Get specific submission details

### Static File Endpoints
- `GET /static/*` - Serve static assets (CSS, JS, images)
- `GET /` - Serve main application interface

## 📊 Analysis Output Structure

```json
{
  "quality_metrics": {
    "summary": "Brief code quality summary",
    "overall_score": 85,
    "cyclomatic_complexity": "Script Complexity: 3.0 (No functions defined)",
    "lines_of_code": 12,
    "time_complexity": "O(n²) - Nested loops detected",
    "space_complexity": "O(1) - Constant space",
    "security_analysis": "No security issues detected",
    "complexity_issues": ["List of complexity-related issues"],
    "security_issues": ["List of security concerns"],
    "recommendations": ["Quality improvement recommendations"]
  },
  "errors": [
    {
      "line": 1,
      "message": "Error description",
      "severity": "error|warning|info"
    }
  ],
  "suggestions": ["AI-generated improvement suggestions"],
  "optimizations": ["Performance optimization recommendations"],
  "output": "Predicted program execution output"
}
```

## 🏗️ Project Structure

```
CodeSense-AI/
├── 📁 static/
│   ├── 📁 css/           # Stylesheets
│   ├── 📁 js/            # Frontend JavaScript
│   │   └── codesense.js  # Main React application
│   └── 📁 images/        # UI images and assets
├── 📁 templates/
│   └── index.html        # Main HTML template
├── 📁 docs/             # Documentation files
├── 📁 code-executor/    # Code execution services
├── 📁 supabase/         # Database configurations
├── 📄 app.py            # Main API routes and logic
├── 📄 main.py           # Application entry point
├── 📄 auth.py           # Authentication logic
├── 📄 database.py       # Database models and setup
├── 📄 logger_config.py  # Logging configuration
├── 📄 requirements.txt  # Python dependencies
└── 📄 .env.example      # Environment variables template
```

## 🔍 Key Features in Detail

### Advanced Complexity Analysis
- **Function-Level Analysis**: Detailed metrics for each function using Lizard
- **Script-Level Analysis**: Handles code without functions (like your nested loop example)
- **Multi-Language Support**: Accurate analysis across different programming languages
- **Fallback Mechanisms**: Robust error handling with alternative analysis methods

### AI-Powered Insights
- **Code Review**: Intelligent suggestions from Google Gemini AI
- **Output Prediction**: Predicts what your code will print or return
- **Security Analysis**: Identifies potential vulnerabilities
- **Best Practices**: Recommendations for code improvement

### Modern UI/UX
- **Collapsible Sections**: Organized results that expand on demand
- **Visual Indicators**: Color-coded quality scores and badges
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Professional Theme**: Coffee-inspired design with workspace imagery

## 🐛 Troubleshooting

### Common Issues

**1. Gemini API Key Issues**
- Ensure your API key is valid and has proper permissions
- Check the `.env` file formatting
- Verify the key is not expired

**2. Complexity Analysis Shows 0.0**
- This is now fixed! The system handles script-level code properly
- For functions: Lizard provides accurate complexity
- For scripts: Custom algorithm calculates complexity

**3. Import Errors**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version compatibility

**4. Database Issues**
- SQLite database is created automatically
- Check file permissions in the project directory
- Database file: `codesense.db` in root directory

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with proper testing
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines
- Follow Python PEP 8 style guide
- Add tests for new features
- Update documentation for API changes
- Ensure all existing tests pass

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent code analysis
- **Lizard** for accurate cyclomatic complexity calculation
- **Monaco Editor** for the excellent code editing experience
- **FastAPI** for the robust backend framework
- **React** for the modern frontend framework

---

**Built with ❤️ for developers who care about code quality**

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
