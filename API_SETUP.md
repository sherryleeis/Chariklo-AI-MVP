# 🔑 API Key Setup Instructions

## The Issue
Your Chariklo app is showing "Claude could not complete this request" because the API key in your `.env` file is invalid or expired.

## Fix Steps

### 1. Get a Valid Anthropic API Key

1. **Go to Anthropic Console**: Visit [console.anthropic.com](https://console.anthropic.com)
2. **Sign Up/Login**: Create an account or log in
3. **Add Credits**: Go to "Billing" and add credits (minimum $5-10 recommended)
4. **Generate API Key**: 
   - Go to "API Keys" section
   - Click "Create Key"
   - Copy the new key (starts with `sk-ant-api03-...`)

### 2. Update Your .env File

Replace the current API key in `/workspaces/Chariklo-AI-MVP/.env`:

```bash
ANTHROPIC_API_KEY=your_new_api_key_here
CLAUDE_API_KEY=your_new_api_key_here
ANTHROPIC_MODEL=claude-3-opus-20240229
```

### 3. Test the Connection

Run this command to verify it works:
```bash
cd /workspaces/Chariklo-AI-MVP && python debug_api.py
```

### 4. Restart Streamlit

After updating the API key:
```bash
streamlit run main.py
```

## Alternative: Use a Different Model

If you want to save costs, you can use a less expensive model by updating your `.env`:

```bash
ANTHROPIC_MODEL=claude-3-haiku-20240307  # Fastest and cheapest
# or
ANTHROPIC_MODEL=claude-3-sonnet-20240229  # Good balance of speed/quality
```

## Security Note

- **Never commit your real API key to GitHub**
- **Keep your .env file in .gitignore**
- **Regenerate keys if they're accidentally exposed**

---

Once you've updated the API key, Chariklo should work perfectly! 🎉
