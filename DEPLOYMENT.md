# Streamlit Cloud Deployment Setup

## Environment Variables
Add these secrets in your Streamlit Cloud app settings:

```
ANTHROPIC_API_KEY = your-actual-anthropic-api-key
CLAUDE_MODEL = claude-3-5-sonnet-20241022
```

## Local Development
1. Create `.streamlit/secrets.toml` with your API keys
2. Run `streamlit run streamlit_app.py`

The secrets.toml file is automatically ignored by git for security.
