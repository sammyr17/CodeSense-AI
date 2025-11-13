"""
CodeSense AI - API Routes
Handles code analysis requests using Google Gemini AI
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import json
import re
import uuid
import time
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from database import get_db, create_code_submission, get_user_submissions, get_submission_by_id, CodeSubmission
from auth import get_current_user, User
from logger_config import setup_logging

# Set up logging
logger = setup_logging(__name__)

# Import Google Generative AI SDK
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

router = APIRouter(prefix="/api", tags=["api"])


class CodeAnalysisRequest(BaseModel):
    code: str
    language: str


class ErrorItem(BaseModel):
    line: int
    message: str
    severity: str


class CodeAnalysisResponse(BaseModel):
    errors: List[ErrorItem]
    suggestions: List[str]
    optimizations: List[str]
    output: str


# --- Debug endpoints ---
@router.get("/debug/ping")
async def debug_ping():
    return {"ok": True}


@router.get("/debug/models")
async def debug_models():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        return JSONResponse(status_code=500, content={"error": "GEMINI_API_KEY is not configured"})
    try:
        # Configure Gemini API and list available models
        genai.configure(api_key=gemini_api_key)
        available_models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
        
        return {"api_provider": "Google Gemini", "count": len(available_models), "models": available_models}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"{e}"})


@router.post("/analyze")
async def analyze_code(
    request: CodeAnalysisRequest, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze code using Google Gemini AI

    Args:
        request: CodeAnalysisRequest containing code and language

    Returns:
        CodeAnalysisResponse with errors, suggestions, optimizations, and output
    """
    if not request.code or not request.language:
        raise HTTPException(
            status_code=400,
            detail="Code and language are required"
        )

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured"
        )

    # Check if Gemini is available
    if not GEMINI_AVAILABLE:
        raise HTTPException(
            status_code=500,
            detail="Google Generative AI library is not installed. Please install it with: pip install google-generativeai"
        )
    
    # Configure Gemini API
    genai.configure(api_key=gemini_api_key)
    
    prompt = f"""Analyze this {request.language} code and return JSON:

```{request.language}
{request.code}
```

Return exactly this JSON format:
{{
  "errors": [{{"line": number, "message": "error description", "severity": "error|warning|info"}}],
  "suggestions": ["suggestion text"],
  "optimizations": ["optimization text"],
  "output": "expected output or 'No output detected'"
}}

Focus on: syntax errors, logic issues, best practices, performance, and expected output. Be concise."""

    try:
        # Use a specific model instead of listing all models
        # This avoids the API call to list_models() which adds latency
        model_name = "models/gemini-flash-latest"  # Available model
        logger.info(f"Using Gemini model: {model_name}")
        model = genai.GenerativeModel(model_name)

        logger.info("Calling Gemini API...")
        api_start_time = time.time()

        # Call Gemini API with optimized settings for speed
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1024,  # Reduced from 4096 for faster response
                temperature=0.1,
                candidate_count=1,  # Only generate one response
            )
        )

        api_end_time = time.time()
        api_duration = api_end_time - api_start_time
        logger.info(f"Gemini API returned response successfully in {api_duration:.2f} seconds")

        # Extract the generated text from Gemini's response
        if not response.text:
            raise HTTPException(
                status_code=500,
                detail="Invalid response from Gemini API"
            )

        generated_text = response.text
        
        # Safe logging for Windows console
        try:
            safe_text = generated_text[:100]
            logger.debug(f"Generated text (first 100 chars): {safe_text}")
        except Exception as e:
            logger.debug(f"Generated text received (encoding safe): {e}")
        
        # Ensure generated_text is a string for regex and parsing
        if not isinstance(generated_text, str):
            generated_text = json.dumps(generated_text)

        # Extract JSON from the response (handle code blocks)
        try:
            json_match = (
                re.search(r'```json\n([\s\S]*?)\n```', generated_text) or
                re.search(r'```\n([\s\S]*?)\n```', generated_text) or
                None
            )
            
            if json_match:
                json_string = json_match.group(1)
            else:
                json_string = generated_text
            
            # json_string must be a string here; attempt to parse
            if isinstance(json_string, str):
                analysis_result = json.loads(json_string)
            else:
                analysis_result = {"output": str(json_string)}
        except (json.JSONDecodeError, AttributeError) as parse_error:
            safe_error = str(parse_error)
            logger.warning(f"Failed to parse Gemini response as JSON: {safe_error}")
            # Fallback response structure
            analysis_result = {
                "errors": [],
                "suggestions": ["AI analysis failed to parse. Please check your code syntax."],
                "optimizations": ["Consider reviewing your code structure."],
                "output": "Analysis unavailable"
            }
        
        # Ensure the response has the expected structure
        errors_list = []
        if isinstance(analysis_result.get("errors"), list):
            for error in analysis_result.get("errors", []):
                if isinstance(error, dict):
                    errors_list.append({
                        "line": error.get("line", 1),
                        "message": error.get("message", "Unknown error"),
                        "severity": error.get("severity", "error")
                    })
        
        result = {
            "errors": errors_list,
            "suggestions": (
                analysis_result.get("suggestions", ["No suggestions available"])
                if isinstance(analysis_result.get("suggestions"), list)
                else ["No suggestions available"]
            ),
            "optimizations": (
                analysis_result.get("optimizations", ["No optimizations suggested"])
                if isinstance(analysis_result.get("optimizations"), list)
                else ["No optimizations suggested"]
            ),
            "output": analysis_result.get("output", "No output detected")
        }
        
        logger.debug(f"Final analysis result: {result}")
        
        # Save code submission to file and database
        try:
            # Create unique filename
            submission_id = str(uuid.uuid4())
            file_extension = {
                'javascript': '.js',
                'python': '.py',
                'java': '.java',
                'cpp': '.cpp',
                'go': '.go'
            }.get(request.language, '.txt')
            
            filename = f"{submission_id}{file_extension}"
            file_path = os.path.join("submissions", filename)
            
            # Save code to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(request.code)
            
            logger.debug(f"Saved code to file: {repr(request.code[:100])}")  # Debug log
            
            # Save submission to database
            create_code_submission(
                db=db,
                user_id=current_user.id,
                language=request.language,
                file_path=file_path,
                analysis_result=json.dumps(result),
                file_name=getattr(request, 'filename', None)
            )
            
            logger.info(f"Saved submission to: {file_path}")
            
        except Exception as save_error:
            logger.warning(f"Failed to save submission: {save_error}")
            # Don't fail the analysis if saving fails
        
        return JSONResponse(status_code=200, content=result)
            
    except HTTPException as he:
        logger.error(f"HTTPException in analyze endpoint: {he.detail}")
        return JSONResponse(status_code=he.status_code, content={
            "detail": f"{he.detail}",
            "errors": [{"line": 1, "message": f"{he.detail}", "severity": "error"}],
            "suggestions": ["Check API key/model access"],
            "optimizations": ["None"],
            "output": "Analysis error"
        })
    except Exception as error:
        import traceback
        error_trace = traceback.format_exc()
        error_msg = str(error)
        logger.error(f"Error in analyze-code function: {error_msg}")
        logger.error(f"Traceback:\n{error_trace}")
        return JSONResponse(status_code=500, content={
            "detail": f"Internal server error: {error_msg}",
            "errors": [{"line": 1, "message": f"Internal server error: {error_msg}", "severity": "error"}],
            "suggestions": ["See server logs for details"],
            "optimizations": ["None"],
            "output": "Analysis error"
        })


# Submission history endpoints
@router.get("/submissions")
async def get_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all submissions for the current user"""
    try:
        submissions = get_user_submissions(db, current_user.id)
        
        # Convert to response format
        submission_list = []
        for submission in submissions:
            submission_data = {
                "id": submission.id,
                "language": submission.language,
                "created_at": submission.created_at.isoformat(),
                "file_name": submission.file_name or f"submission.{submission.language}"
            }
            submission_list.append(submission_data)
        
        return JSONResponse(status_code=200, content={"submissions": submission_list})
        
    except Exception as e:
        logger.error(f"Error fetching submissions: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to fetch submissions"})


@router.get("/submissions/{submission_id}")
async def get_submission(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific submission with code and analysis results"""
    try:
        submission = get_submission_by_id(db, submission_id, current_user.id)
        
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        # Read code from file
        try:
            with open(submission.file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            logger.debug(f"Read code from file: {repr(code_content[:100])}")  # Debug log
        except FileNotFoundError:
            code_content = "Code file not found"
        
        # Parse analysis result
        analysis_result = {}
        if submission.analysis_result:
            try:
                analysis_result = json.loads(submission.analysis_result)
            except json.JSONDecodeError:
                analysis_result = {"error": "Failed to parse analysis result"}
        
        response_data = {
            "id": submission.id,
            "language": submission.language,
            "code": code_content,
            "analysis_result": analysis_result,
            "created_at": submission.created_at.isoformat(),
            "file_name": submission.file_name or f"submission.{submission.language}"
        }
        
        return JSONResponse(status_code=200, content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching submission {submission_id}: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to fetch submission"})