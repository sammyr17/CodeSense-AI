"""
CodeSense AI - Main Entry Point
A Python web application for AI-powered code analysis
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from app import router
from auth import auth_router
from database import create_database_and_tables, test_database_connection
from logger_config import setup_logging

# Set up logging
logger = setup_logging(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="CodeSense AI",
    description="AI-Powered Code Analysis Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)
app.include_router(auth_router)

# Serve static files (CSS/JS files)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Error: templates/index.html not found</h1>",
            status_code=404
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting CodeSense AI on http://localhost:{port}")
    logger.info("Make sure GEMINI_API_KEY is set in .env file")
    
    # Initialize database
    logger.info("Initializing database...")
    try:
        if test_database_connection():
            create_database_and_tables()
            logger.info("Database initialized successfully")
        else:
            logger.warning("Database connection failed - authentication features may not work")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        logger.warning("Authentication features may not work - please check PostgreSQL connection")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )