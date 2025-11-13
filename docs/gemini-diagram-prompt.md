# Gemini Prompt for CodeSense AI System Architecture Diagram

## Copy this prompt to Gemini:

---

**Create a high-level system architecture diagram for "CodeSense AI" - a web-based code analysis platform. Generate a clean, professional diagram with the following specifications:**

## Visual Requirements:
- **Style**: Clean, modern, professional architecture diagram
- **Colors**: Use blue tones for frontend, green for backend, orange for AI services, gray for data storage
- **Layout**: Top-to-bottom flow with clear component separation
- **Shapes**: Rectangles for components, cylinders for databases, clouds for external services
- **Arrows**: Solid arrows for data flow, dashed arrows for API calls

## Components to Include:

### 1. User Layer (Top)
- **Shape**: Rectangle with rounded corners
- **Color**: Light blue (#E3F2FD)
- **Content**: "User Browser" with sub-components:
  - Web Browser
  - User Interface

### 2. Frontend Layer
- **Shape**: Large rectangle
- **Color**: Blue (#2196F3)
- **Title**: "React SPA Frontend"
- **Sub-components** (smaller rectangles inside):
  - Monaco Code Editor
  - Authentication UI (Login/Signup)
  - Analysis Results Display
  - Past Submissions History
  - Report Generation

### 3. Backend API Layer
- **Shape**: Large rectangle
- **Color**: Green (#4CAF50)
- **Title**: "FastAPI Backend Server"
- **Sub-components**:
  - Authentication Service (/auth/*)
  - Code Analysis API (/api/analyze)
  - User Management (/api/users)
  - Submissions API (/api/submissions)
  - Static File Server (/static/*)

### 4. AI Processing Layer
- **Shape**: Cloud shape
- **Color**: Orange (#FF9800)
- **Title**: "Google Gemini AI"
- **Sub-components**:
  - Code Analysis Engine
  - Natural Language Processing
  - Multi-language Support

### 5. Data Storage Layer
- **Shape**: Cylinder (database symbol)
- **Color**: Gray (#757575)
- **Components**:
  - SQLite Database (Users, Submissions)
  - File System (Code Files, Reports)

## Connections & Data Flow:

### Arrows to draw:
1. **User Browser → React Frontend**: Bidirectional solid arrow (HTTP/HTTPS)
2. **React Frontend → FastAPI Backend**: Bidirectional solid arrow (REST API calls)
3. **FastAPI Backend → Google Gemini**: Dashed arrow (API calls)
4. **Google Gemini → FastAPI Backend**: Dashed arrow (AI responses)
5. **FastAPI Backend → SQLite Database**: Bidirectional solid arrow (CRUD operations)
6. **FastAPI Backend → File System**: Bidirectional solid arrow (File I/O)

## Labels for Arrows:
- "HTTP/HTTPS Requests" (User ↔ Frontend)
- "REST API Calls" (Frontend ↔ Backend)
- "AI Analysis Requests" (Backend → Gemini)
- "Analysis Results" (Gemini → Backend)
- "Database Queries" (Backend ↔ Database)
- "File Operations" (Backend ↔ File System)

## Additional Details:

### Technology Stack Labels:
- Frontend: "React 18, Monaco Editor, Tailwind CSS"
- Backend: "FastAPI, Python, JWT Authentication"
- AI: "Google Gemini Flash API"
- Database: "SQLite, SQLAlchemy ORM"

### Security Features (add as small icons/badges):
- JWT Authentication
- Password Hashing (bcrypt)
- CORS Configuration
- Input Validation

### Supported Languages (add as small badges):
- JavaScript, Python, Java, C++, Go

## Layout Instructions:
1. Arrange components in vertical layers from top to bottom
2. Use consistent spacing between layers
3. Center-align all components
4. Add a title at the top: "CodeSense AI - System Architecture"
5. Include a legend showing what each color represents
6. Add version/date in bottom corner

## Final Touches:
- Add subtle shadows to components for depth
- Use consistent font sizes (larger for main components, smaller for sub-components)
- Include small icons where appropriate (code icon, database icon, cloud icon)
- Make sure all text is readable and professional

**Generate this as a clear, high-resolution diagram that could be used in technical documentation or presentations.**

---
