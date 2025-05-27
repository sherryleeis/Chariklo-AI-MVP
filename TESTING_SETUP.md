# Chariklo Testing Setup Guide

## Quick Start

### Prerequisites
- Python 3.11+
- Anthropic API key

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sherryleeis/Chariklo-AI-MVP.git
   cd Chariklo-AI-MVP
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file in the root directory:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ANTHROPIC_MODEL=claude-3-opus-20240229
   ```

4. Run Chariklo:
   ```bash
   streamlit run main.py
   ```

## What to Test

### Core Functionality
- **Presence Quality**: Does Chariklo feel genuinely present vs. performing helpfulness?
- **Response Length**: Are responses appropriately brief (1-2 sentences mostly)?
- **Natural Flow**: Does conversation feel organic vs. scripted?
- **Insight Emergence**: Do you discover things vs. being told things?

### Specific Features to Try
- **Audio cues**: Try asking for `[[bell]]`, `[[rain-30]]`, etc.
- **Memory system**: Toggle memory on/off and see how it affects conversation
- **Reflection logging**: Use "Run analysis on latest session" to see system insights
- **Natural completion**: Notice how conversations end organically

### What We're Looking For
- Moments of genuine connection vs. AI helpfulness
- Times when you feel truly seen/witnessed
- Instances where insights arise naturally in you
- Overall sense of authentic presence

### Feedback Areas
- **Presence authenticity**: When does it feel real vs. performed?
- **Response appropriateness**: Length, tone, timing
- **System behavior**: Any bugs, errors, or unexpected responses
- **User experience**: What supports your process vs. what feels intrusive?

## Known Constraints
- Requires Anthropic API key (Claude 3 Opus recommended)
- Audio features require browser audio permissions
- Memory system is basic but functional

## Support
Create issues on GitHub or share feedback directly for system refinement.
