# Migration from Claude to Gemini API

## Changes Made

### 1. Dependencies Updated
- Removed: `anthropic==0.72.1`
- Added: `google-generativeai==0.8.3`

### 2. Environment Variables
- **Old**: `ANTHROPIC_API_KEY`
- **New**: `GEMINI_API_KEY`

### 3. API Changes
- Replaced Anthropic Claude API calls with Google Gemini API calls
- Updated model from `claude-3-5-sonnet-20241022` to `gemini-1.5-pro`
- Updated error handling and response parsing for Gemini format

### 4. Files Modified
- `app.py` - Main API logic updated
- `requirements.txt` - Dependencies updated (backup created as `requirements_new.txt`)
- `.env.example` - Already configured for Gemini

## Setup Instructions

1. **Install new dependencies:**
   ```bash
   pip install -r requirements_new.txt
   ```

2. **Set up environment variable:**
   - Copy `.env.example` to `.env`
   - Get your Gemini API key from: https://makersuite.google.com/app/apikey
   - Replace `your_gemini_api_key_here` with your actual API key

3. **Remove old environment variable:**
   - Delete or comment out `ANTHROPIC_API_KEY` from your `.env` file

## Benefits of Gemini API

- **Tier 1 Subscription**: Better rate limits and performance
- **Cost Effective**: Generally more affordable than Claude
- **Latest Models**: Access to Google's latest Gemini models
- **Better Integration**: Native Google ecosystem integration

## Testing

After setup, test the migration:
1. Start the server: `python main.py`
2. Visit: `http://localhost:8000/api/debug/models`
3. Should return Gemini models instead of Claude models
4. Test code analysis at: `http://localhost:8000/api/analyze`
