# LatticeFlow

LatticeFlow is a modular, conversational journaling and workout system built with Streamlit. It features:
- AM/PM journaling flows (conversational UI, GPT scoring/tagging)
- Workout tracking with RPE sidebar and last week's log reference
- Macro cheat sheet with label scanning (OCR-ready)
- Memory board (cards)
- ADHD toolkits (pop-ups)
- Simple password authentication

## Getting Started

1. Clone this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Project Structure
- `streamlit_app.py` — Main entry point
- `plan.md` — Centralized planning and system canvas
- `requirements.txt` — Python dependencies
- `.gitignore` — Ignore system, secret, and cache files
- `.replit` — (Optional) Replit run command

## Environment Variables
- Place API keys and secrets in `.env` or `.streamlit/secrets.toml` (never commit secrets)

## License
MIT
