# 🌟 Chariklo: AI for Inner Space

Chariklo is a presence-based AI companion designed for inner exploration, self-reflection, and contemplative dialogue. Unlike typical chatbots, Chariklo offers a spacious, non-judgmental presence that supports deep inquiry and personal insight.

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chariklo.streamlit.app/)

## ✨ Features

- **Presence-based responses** with mindful timing and tone
- **Memory system** that learns and remembers important moments
- **Contemplative dialogue** focused on inner exploration
- **Beautiful mobile-friendly interface** 
- **Comprehensive feedback system** for continuous improvement

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
1. Get an API key from [console.anthropic.com](https://console.anthropic.com)
2. Create `.env` file:
```bash
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-opus-20240229
```

### 3. Test Connection
```bash
python validate_api.py
```

### 4. Run App
```bash
streamlit run main.py
```

## 📖 Documentation

- **[API_SETUP.md](API_SETUP.md)** - Detailed API key setup instructions
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Streamlit Cloud deployment guide
- **[TESTING_SETUP.md](TESTING_SETUP.md)** - Testing and feedback guidelines

## 🔧 Troubleshooting

**"Claude could not complete this request"**
- Check your API key with: `python validate_api.py`
- Ensure your Anthropic account has credits
- See [API_SETUP.md](API_SETUP.md) for detailed instructions

**Connection issues**
- Verify internet connection
- Check if you've hit rate limits
- Try a different Claude model in `.env`

## 💝 Contributing

Chariklo is designed as a contemplative tool. When contributing:
- Maintain the calm, spacious tone
- Test with real inner exploration scenarios  
- Focus on presence over productivity

---

*"In the space between stimulus and response lies our freedom and power to choose our response. In our response lies our growth and happiness." - Viktor Frankl*
