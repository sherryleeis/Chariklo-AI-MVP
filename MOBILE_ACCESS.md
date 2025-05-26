📱 **MOBILE ACCESS INSTRUCTIONS**

## 🔗 URLs to Try on Your Phone:

### Local Development (if on same network):
- `http://172.191.151.50:8503`
- `http://localhost:8503` (if using port forwarding)

### Streamlit Cloud (if deployed):
- Check your Streamlit Cloud dashboard
- Make sure environment variables are updated there

---

## 🚨 Most Likely Issue: Streamlit Cloud Environment

If you're accessing via Streamlit Cloud, the issue is probably that **your API key isn't set in the cloud environment**. Here's how to fix it:

### 1. Go to Streamlit Cloud Dashboard
- Visit [share.streamlit.io](https://share.streamlit.io)
- Find your Chariklo app

### 2. Update Environment Variables
- Click on your app
- Go to "Settings" → "Secrets"
- Add this:
```toml
ANTHROPIC_API_KEY = "your-actual-api-key-here"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"
```

### 3. Restart Your App
- Click "Reboot app" in Streamlit Cloud
- Wait for it to redeploy

---

## 🧹 Clear Mobile Cache

1. **Force refresh** on mobile browser
2. **Clear browser cache** for the site
3. **Try incognito/private mode**

---

## 🔧 Quick Test

Try this URL on your phone to see if the local version works:
http://172.191.151.50:8503

If that doesn't work, the issue is definitely with your Streamlit Cloud deployment needing the API key update.
