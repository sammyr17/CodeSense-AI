# CodeSense AI - High-Level System Architecture

## Overview
CodeSense AI is a web-based code analysis platform that leverages Google Gemini AI to provide intelligent code review, optimization suggestions, and multi-language support.

## Architecture Components

### 1. Frontend Layer (React SPA)
```
┌─────────────────────────────────────────┐
│              Frontend (React)           │
├─────────────────────────────────────────┤
│ • Monaco Editor (Code Input)            │
│ • Authentication UI (Login/Signup)      │
│ • Analysis Results Display              │
│ • Past Submissions History              │
│ • Multi-language Support UI            │
│ • Report Generation & Download          │
└─────────────────────────────────────────┘
```

### 2. Backend API Layer (FastAPI)
```
┌─────────────────────────────────────────┐
│            Backend API (FastAPI)        │
├─────────────────────────────────────────┤
│ • Authentication Endpoints              │
│ • Code Analysis API                     │
│ • User Management                       │
│ • Submission History                    │
│ • File Upload/Download                  │
│ • Static File Serving                   │
└─────────────────────────────────────────┘
```

### 3. AI Processing Layer
```
┌─────────────────────────────────────────┐
│          AI Processing Layer            │
├─────────────────────────────────────────┤
│ • Google Gemini API Integration         │
│ • Code Analysis Prompts                 │
│ • Response Processing                   │
│ • Error Handling & Retry Logic         │
└─────────────────────────────────────────┘
```

### 4. Data Layer
```
┌─────────────────────────────────────────┐
│              Data Layer                 │
├─────────────────────────────────────────┤
│ • SQLite Database (User Data)           │
│ • File System (Code Submissions)       │
│ • Session Management                    │
│ • User Authentication Data              │
└─────────────────────────────────────────┘
```

## System Flow Diagram

```
User Browser
     │
     ▼
┌─────────────────┐    HTTP/HTTPS    ┌─────────────────┐
│   React SPA     │ ◄──────────────► │   FastAPI       │
│                 │                  │   Backend       │
│ • Monaco Editor │                  │                 │
│ • Auth Forms    │                  │ • /api/analyze  │
│ • Results UI    │                  │ • /auth/*       │
└─────────────────┘                  │ • /api/submit*  │
                                     └─────────────────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │  Google Gemini  │
                                     │      API        │
                                     │                 │
                                     │ • Code Analysis │
                                     │ • AI Processing │
                                     └─────────────────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │   Data Storage  │
                                     │                 │
                                     │ • SQLite DB     │
                                     │ • File System   │
                                     └─────────────────┘
```

## Detailed Component Breakdown

### Frontend Components
- **Authentication**: Login/Signup forms with JWT token management
- **Code Editor**: Monaco Editor with syntax highlighting for multiple languages
- **Analysis Interface**: Real-time code analysis with AI-powered suggestions
- **History Management**: View and manage past code submissions
- **Report Generation**: Download analysis reports in text format

### Backend Services
- **Authentication Service**: JWT-based user authentication and authorization
- **Code Analysis Service**: Integration with Google Gemini AI for code review
- **File Management**: Save/retrieve code submissions and analysis results
- **User Management**: CRUD operations for user accounts
- **API Gateway**: RESTful API endpoints for frontend communication

### Database Schema
```
Users Table:
- id (Primary Key)
- username (Unique)
- email
- password_hash
- full_name
- created_at

Code_Submissions Table:
- id (Primary Key)
- user_id (Foreign Key)
- language
- file_path
- analysis_result (JSON)
- file_name
- created_at
```

### Security Features
- **Password Hashing**: bcrypt for secure password storage
- **JWT Authentication**: Secure token-based authentication
- **CORS Configuration**: Cross-origin resource sharing setup
- **Input Validation**: Request validation and sanitization
- **Error Handling**: Comprehensive error handling and logging

### Supported Languages
- JavaScript
- Python
- Java
- C++
- Go
- (Extensible for additional languages)

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Production Environment                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Nginx     │    │   FastAPI   │    │   SQLite    │  │
│  │ (Reverse    │◄──►│   Server    │◄──►│  Database   │  │
│  │  Proxy)     │    │             │    │             │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Static Files                           │  │
│  │  • React Build Files                                │  │
│  │  • CSS/JS Assets                                    │  │
│  │  • Images                                           │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## External Dependencies
- **Google Gemini API**: AI-powered code analysis
- **Monaco Editor CDN**: Code editor functionality
- **React/ReactDOM CDN**: Frontend framework
- **Tailwind CSS CDN**: Styling framework
- **Babel Standalone**: JSX transformation

## Performance Considerations
- **Caching**: Static file caching for improved load times
- **Async Processing**: Non-blocking AI API calls
- **Error Recovery**: Graceful handling of API failures
- **Resource Management**: Efficient file storage and cleanup
- **Rate Limiting**: API rate limiting for stability

## Monitoring & Logging
- **Application Logs**: Comprehensive logging for debugging
- **Error Tracking**: Exception handling and reporting
- **Performance Metrics**: Response time monitoring
- **User Analytics**: Usage patterns and feature adoption
