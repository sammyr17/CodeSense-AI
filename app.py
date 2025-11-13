"""
CodeSense AI - API Routes
Handles code analysis requests using Google Gemini AI
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import json
import re
from typing import Optional, List, Dict

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
async def analyze_code(request: CodeAnalysisRequest):
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

    # Configure Gemini API
    genai.configure(api_key=gemini_api_key)
    
    prompt = f"""Analyze the following {request.language} code and provide a comprehensive analysis in JSON format. 

Code to analyze:
```{request.language}
{request.code}
```

Please provide your response in this exact JSON structure:
{{
  "errors": [
    {{
      "line": number,
      "message": "description of the error",
      "severity": "error" | "warning" | "info"
    }}
  ],
  "suggestions": [
    "suggestion 1",
    "suggestion 2"
  ],
  "optimizations": [
    "optimization 1",
    "optimization 2"
  ],
  "output": "expected output or 'No output detected'"
}}

Focus on:
1. Syntax errors, logic errors, and potential runtime issues
2. Best practices and code quality improvements  
3. Performance optimizations and cleaner code suggestions
4. What the code output would be (if any print/console statements exist)

Be thorough but concise. Only include actual issues, not hypothetical ones."""

    try:
        # Get the first available model that supports generateContent
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if not available_models:
            raise HTTPException(
                status_code=500,
                detail="No available Gemini models found that support generateContent"
            )
        
        # Use the first available model
        model_name = available_models[0]
        print(f"Using model: {model_name}")
        model = genai.GenerativeModel(model_name)

        print("Calling Gemini API...")

        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=4096,
                temperature=0.1,
            )
        )

        # Extract the generated text from Gemini's response
        if not response.text:
            raise HTTPException(
                status_code=500,
                detail="Invalid response from Gemini API"
            )

        generated_text = response.text
        print(f"[SUCCESS] Gemini API returned response")
        
        # Safe print for Windows console
        try:
            safe_text = generated_text[:100]
            print(f"Generated text (first 100 chars): {safe_text}")
        except:
            print("Generated text received (encoding safe)")
        
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
            print(f"Failed to parse Gemini response as JSON: {safe_error}")
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
        
        print(f"Final analysis result: {result}")
        return JSONResponse(status_code=200, content=result)
            
    except HTTPException as he:
        print(f"[ERROR] HTTPException: {he.detail}")
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
        print(f"[ERROR] Error in analyze-code function:")
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Traceback:\n{error_trace}")
        return JSONResponse(status_code=500, content={
            "detail": f"Internal server error: {error_msg}",
            "errors": [{"line": 1, "message": f"Internal server error: {error_msg}", "severity": "error"}],
            "suggestions": ["See server logs for details"],
            "optimizations": ["None"],
            "output": "Analysis error"
        })