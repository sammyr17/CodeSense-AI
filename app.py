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
import tempfile
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from database import get_db, create_code_submission, get_user_submissions, get_submission_by_id, CodeSubmission
from auth import get_current_user, User
from logger_config import setup_logging
import lizard

# Set up logging
logger = setup_logging(__name__)

# Import Google Generative AI SDK
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

router = APIRouter(prefix="/api", tags=["api"])
auth_router = APIRouter(prefix="/auth")

def analyze_code_complexity(code: str, language: str) -> Dict:
    """
    Analyze code complexity using Lizard library
    """
    try:
        # Create a temporary file with appropriate extension
        file_extension = {
            'javascript': '.js',
            'python': '.py',
            'java': '.java',
            'cpp': '.cpp',
            'c': '.c',
            'go': '.go'
        }.get(language, '.txt')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix=file_extension, delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        # Analyze with Lizard
        analysis = lizard.analyze_file(temp_file_path)
        
        # Clean up temp file
        os.unlink(temp_file_path)
        
        # Calculate metrics
        total_functions = len(analysis.function_list)
        total_complexity = sum(func.cyclomatic_complexity for func in analysis.function_list)
        avg_complexity = total_complexity / total_functions if total_functions > 0 else 0
        max_complexity = max((func.cyclomatic_complexity for func in analysis.function_list), default=0)
        
        # Handle script-level complexity (when no functions are defined)
        script_complexity = 0
        if total_functions == 0:
            script_complexity = calculate_script_complexity(code, language)
            avg_complexity = script_complexity
            max_complexity = script_complexity
        
        # Estimate time and space complexity based on code patterns
        time_complexity = estimate_time_complexity(code, language)
        space_complexity = estimate_space_complexity(code, language)
        
        # Calculate overall score (0-100)
        overall_score = calculate_overall_score(
            avg_complexity, max_complexity, max(total_functions, 1), 
            analysis.nloc, time_complexity, space_complexity
        )
        
        complexity_description = ""
        if total_functions > 0:
            complexity_description = f"Average: {avg_complexity:.1f}, Max: {max_complexity}, Total Functions: {total_functions}"
        else:
            complexity_description = f"Script Complexity: {script_complexity:.1f} (No functions defined)"
        
        return {
            "cyclomatic_complexity": complexity_description,
            "lines_of_code": analysis.nloc,
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "overall_score": overall_score,
            "complexity_details": {
                "average_complexity": avg_complexity,
                "max_complexity": max_complexity,
                "total_functions": total_functions,
                "script_complexity": script_complexity,
                "lines_of_code": analysis.nloc
            }
        }
        
    except Exception as e:
        logger.warning(f"Lizard analysis failed: {e}")
        # Fallback to script-level complexity calculation
        try:
            script_complexity = calculate_script_complexity(code, language)
            time_complexity = estimate_time_complexity(code, language)
            space_complexity = estimate_space_complexity(code, language)
            lines_count = len([line for line in code.split('\n') if line.strip()])
            
            overall_score = calculate_overall_score(
                script_complexity, script_complexity, 1, 
                lines_count, time_complexity, space_complexity
            )
            
            return {
                "cyclomatic_complexity": f"Script Complexity: {script_complexity:.1f} (Lizard failed, using fallback)",
                "lines_of_code": lines_count,
                "time_complexity": time_complexity,
                "space_complexity": space_complexity,
                "overall_score": overall_score,
                "complexity_details": {
                    "script_complexity": script_complexity,
                    "lines_of_code": lines_count
                }
            }
        except Exception as fallback_error:
            logger.error(f"Fallback complexity analysis also failed: {fallback_error}")
            return {
                "cyclomatic_complexity": "Analysis failed",
                "lines_of_code": 0,
                "time_complexity": "Unable to determine",
                "space_complexity": "Unable to determine", 
                "overall_score": 50,
                "complexity_details": {}
            }

def calculate_script_complexity(code: str, language: str) -> float:
    """
    Calculate cyclomatic complexity for script-level code (no functions)
    """
    complexity = 1  # Base complexity
    code_lower = code.lower()
    
    # Count decision points that increase complexity
    if language == 'python':
        # Control flow statements
        complexity += code_lower.count('if ')
        complexity += code_lower.count('elif ')
        complexity += code_lower.count('for ')
        complexity += code_lower.count('while ')
        complexity += code_lower.count('except ')
        complexity += code_lower.count('and ')
        complexity += code_lower.count('or ')
        complexity += code_lower.count('break')
        complexity += code_lower.count('continue')
        
    elif language == 'javascript':
        complexity += code_lower.count('if(') + code_lower.count('if (')
        complexity += code_lower.count('else if') + code_lower.count('elseif')
        complexity += code_lower.count('for(') + code_lower.count('for (')
        complexity += code_lower.count('while(') + code_lower.count('while (')
        complexity += code_lower.count('switch')
        complexity += code_lower.count('case ')
        complexity += code_lower.count('catch')
        complexity += code_lower.count('&&')
        complexity += code_lower.count('||')
        complexity += code_lower.count('break')
        complexity += code_lower.count('continue')
        
    elif language in ['java', 'cpp', 'c']:
        complexity += code_lower.count('if(') + code_lower.count('if (')
        complexity += code_lower.count('else if')
        complexity += code_lower.count('for(') + code_lower.count('for (')
        complexity += code_lower.count('while(') + code_lower.count('while (')
        complexity += code_lower.count('switch')
        complexity += code_lower.count('case ')
        complexity += code_lower.count('catch')
        complexity += code_lower.count('&&')
        complexity += code_lower.count('||')
        complexity += code_lower.count('break')
        complexity += code_lower.count('continue')
        
    elif language == 'go':
        complexity += code_lower.count('if ')
        complexity += code_lower.count('for ')
        complexity += code_lower.count('switch')
        complexity += code_lower.count('case ')
        complexity += code_lower.count('select')
        complexity += code_lower.count('&&')
        complexity += code_lower.count('||')
        complexity += code_lower.count('break')
        complexity += code_lower.count('continue')
    
    return float(complexity)

def estimate_time_complexity(code: str, language: str) -> str:
    """
    Estimate time complexity based on code patterns
    """
    code_lower = code.lower()
    
    # Count nested loops
    nested_loops = 0
    if language == 'python':
        nested_loops = code_lower.count('for') + code_lower.count('while')
    elif language == 'javascript':
        nested_loops = code_lower.count('for') + code_lower.count('while')
    elif language in ['java', 'cpp', 'c']:
        nested_loops = code_lower.count('for(') + code_lower.count('while(')
    
    # Check for recursive patterns
    has_recursion = 'recursion' in code_lower or code_lower.count('return') > 1
    
    # Estimate based on patterns
    if nested_loops >= 3:
        return "O(n³) or higher - Multiple nested loops detected"
    elif nested_loops == 2:
        return "O(n²) - Nested loops detected"
    elif nested_loops == 1:
        return "O(n) - Single loop detected"
    elif has_recursion:
        return "O(log n) to O(n) - Recursive pattern detected"
    else:
        return "O(1) - Constant time operations"

def estimate_space_complexity(code: str, language: str) -> str:
    """
    Estimate space complexity based on code patterns
    """
    code_lower = code.lower()
    
    # Check for data structures
    arrays = code_lower.count('array') + code_lower.count('list') + code_lower.count('[]')
    objects = code_lower.count('object') + code_lower.count('dict') + code_lower.count('{}')
    
    # Check for recursive calls (stack space)
    has_recursion = 'recursion' in code_lower or code_lower.count('return') > 1
    
    if arrays > 2 or objects > 2:
        return "O(n) - Multiple data structures"
    elif arrays > 0 or objects > 0:
        return "O(n) - Data structures used"
    elif has_recursion:
        return "O(log n) to O(n) - Recursive stack space"
    else:
        return "O(1) - Constant space"

def calculate_overall_score(avg_complexity: float, max_complexity: int, 
                          total_functions: int, lines_of_code: int,
                          time_complexity: str, space_complexity: str) -> int:
    """
    Calculate overall code quality score (0-100)
    """
    score = 100
    
    # Complexity penalty
    if avg_complexity > 10:
        score -= 30
    elif avg_complexity > 5:
        score -= 15
    elif avg_complexity > 3:
        score -= 5
    
    # Max complexity penalty
    if max_complexity > 15:
        score -= 25
    elif max_complexity > 10:
        score -= 15
    elif max_complexity > 5:
        score -= 5
    
    # Lines of code penalty (too long functions)
    if lines_of_code > 200:
        score -= 15
    elif lines_of_code > 100:
        score -= 10
    elif lines_of_code > 50:
        score -= 5
    
    # Time complexity penalty
    if "O(n³)" in time_complexity or "higher" in time_complexity:
        score -= 20
    elif "O(n²)" in time_complexity:
        score -= 10
    elif "O(n)" in time_complexity and "nested" not in time_complexity.lower():
        score -= 5
    
    # Bonus for good practices
    if total_functions > 0 and avg_complexity <= 3:
        score += 5
    if lines_of_code > 0 and lines_of_code <= 50:
        score += 5
    
    return max(0, min(100, score))

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
  "output": "predicted program output",
  "quality_metrics": {{
    "summary": "brief summary of code quality",
    "complexity_issues": ["issue_1", "issue_2"],
    "security_issues": ["issue_1", "issue_2"],
    "recommendations": ["recommendation_1", "recommendation_2"],
    "security_analysis": "security assessment summary"
  }}
}}

Instructions:
1. Check for syntax errors, logic issues, and best practices
2. For the "output" field: If the code contains print statements, loops, or calculations, predict what would be printed to console when executed
3. If the code doesn't produce console output, set output to "No console output"
4. For loops, show the expected iteration results
5. Be precise with output prediction - show exactly what would appear in the terminal
6. For quality_metrics: Analyze code complexity, maintainability, security issues, and provide actionable recommendations
7. Estimate cyclomatic complexity based on control flow structures (if/else, loops, functions)
8. Assess maintainability based on code structure, naming, and organization
9. Identify potential security vulnerabilities (SQL injection, XSS, unsafe operations, etc.)

Example: For a loop that prints numbers, show each line that would be printed."""

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

        # Check if response was blocked or has issues
        if not response.candidates:
            logger.error("No candidates returned from Gemini API")
            raise HTTPException(
                status_code=500,
                detail="No response candidates from Gemini API"
            )
        
        candidate = response.candidates[0]
        
        # Check finish reason
        if candidate.finish_reason == 2:  # SAFETY
            logger.warning("Gemini response blocked due to safety filters")
            # Return a safe fallback response
            analysis_result = {
                "errors": [],
                "suggestions": ["Code analysis was blocked by safety filters. Please ensure your code doesn't contain sensitive content."],
                "optimizations": ["Try simplifying your code or removing any potentially sensitive content."],
                "output": "Analysis blocked by safety filters"
            }
        elif candidate.finish_reason == 3:  # RECITATION
            logger.warning("Gemini response blocked due to recitation")
            analysis_result = {
                "errors": [],
                "suggestions": ["Code analysis was blocked due to content similarity. Try modifying your code slightly."],
                "optimizations": ["Consider using different variable names or restructuring your code."],
                "output": "Analysis blocked due to content similarity"
            }
        elif candidate.finish_reason != 1:  # Not STOP (successful completion)
            logger.warning(f"Gemini response finished with reason: {candidate.finish_reason}")
            analysis_result = {
                "errors": [],
                "suggestions": ["Code analysis completed with warnings. Results may be incomplete."],
                "optimizations": ["Try running the analysis again or simplifying your code."],
                "output": "Analysis completed with warnings"
            }
        else:
            # Normal successful response
            try:
                generated_text = response.text
            except ValueError as e:
                logger.error(f"Failed to extract text from Gemini response: {e}")
                analysis_result = {
                    "errors": [],
                    "suggestions": ["Unable to extract analysis results from AI response."],
                    "optimizations": ["Try running the analysis again."],
                    "output": "Unable to extract analysis results"
                }
            else:
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
                    logger.debug(f"Raw Gemini response: {repr(generated_text[:500])}")
                    
                    # Try to extract useful information from the raw response
                    output_prediction = "Unable to predict output"
                    if "print" in request.code.lower() or "console.log" in request.code.lower():
                        output_prediction = "Code contains output statements but prediction failed"
                    elif any(keyword in request.code.lower() for keyword in ["for", "while", "loop"]):
                        output_prediction = "Code contains loops but output prediction failed"
                    
                    # Fallback response structure
                    analysis_result = {
                        "errors": [],
                        "suggestions": ["AI analysis completed but response format was unexpected."],
                        "optimizations": ["Consider reviewing your code structure."],
                        "output": output_prediction
                    }
        
        # Analyze code complexity with Lizard
        complexity_analysis = analyze_code_complexity(request.code, request.language)
        
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
        
        # Merge Gemini analysis with Lizard complexity analysis
        quality_metrics = analysis_result.get("quality_metrics", {})
        quality_metrics.update({
            "cyclomatic_complexity": complexity_analysis["cyclomatic_complexity"],
            "time_complexity": complexity_analysis["time_complexity"],
            "space_complexity": complexity_analysis["space_complexity"],
            "overall_score": complexity_analysis["overall_score"],
            "lines_of_code": complexity_analysis["lines_of_code"]
        })
        
        # Ensure default values for missing fields
        quality_metrics.setdefault("summary", "Quality analysis completed")
        quality_metrics.setdefault("complexity_issues", [])
        quality_metrics.setdefault("security_issues", [])
        quality_metrics.setdefault("recommendations", [])
        quality_metrics.setdefault("security_analysis", "No security issues detected")
        
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
            "output": analysis_result.get("output", "No console output predicted"),
            "quality_metrics": quality_metrics
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
            
            # Save submission to databases
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