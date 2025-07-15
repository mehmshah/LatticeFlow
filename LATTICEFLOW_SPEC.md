# LatticeFlow System Specification & Replit Deployment Guide

---

## 1. Overview

LatticeFlow is a modular journaling and physical/mental maintenance system with conversational UI, robust export/summarization, and extensible modules for nutrition, ADHD, and more. The app is designed for clarity, trend analysis, and future AI integration.

---

## 2. Navigation & UX

- **Hybrid Navigation:**  
  - Landing dashboard with cards/stats for each module.
  - Persistent, collapsible sidebar for instant navigation.
- **Light/Dark Mode:**  
  - User-toggleable.
- **Authentication:**  
  - Simple password login for MVP.
- **Export/Download:**  
  - All logs exportable as Markdown and JSON, per entry, with metadata.
- **Scheduled Summaries:**  
  - Automatic weekly/monthly summary files per module and globally.
  - “Summarize My Data” button for on-demand summaries.
  - Summaries include stats, trends, highlights, and GPT-powered natural language overviews.

---

## 3. Module Specifications

### Mental Maintenance (Journaling)
- Chat card per section, free text, button prompts for guidance.
- ADHD pop-ups in AM routine via button prompt.
- Prompts for sleep, energy, ADHD scripts, prior focus, intentions.
- Chat history saved in Markdown/JSON.
- GPT API for scoring, tagging, summaries.
- Metric anchors for 30+ scores.
- Macro log in PM routine, searchable, supports natural language and photo OCR.
- Future: psychologist/therapist notes, tagged/categorized.

### Physical Maintenance (Workout Tracking)
- Landing: list/grid of templates + “+ New Workout”.
- Logging: screenshot uploads (OCR) and manual entry.
- Custom workout templates, editable categories.
- UI: line per set, checkboxes (completion), textboxes (reps, RPE).
- RPE suggestions in sidebar, exercise suggestions inline.
- Auto-generated tags (no manual).
- Export to JSON/Markdown.
- General log for physio/doctor/chiro notes, append-only, improved tagging.
- Diet tracking as tab/section: daily macro summaries, grocery “snapshot”, natural language + photo OCR, supports you & wife.

### Nutrition Module
- Macro cheat sheet linked to PM macro log.
- Recipe ideas, grocery tracking, butchering ideas, mass food prep.
- Meat CSA sourcing notes.

### ADHD Toolkit
- List of scripts/toolkits, add/edit/display.
- Clicking item opens pop-up/sidebar.
- No categories/favoriting for MVP.
- Scripts can surface in AM review.

---

## 4. Data, Export, and Summarization

- **Auto-Export:**  
  - Logs auto-exported as Markdown/JSON per entry, with metadata.
- **Scheduled Summaries:**  
  - Weekly/monthly summary files per module and globally.
  - Summaries: key stats/trends, highlights, GPT-powered summary.
  - Saved in dedicated folder, downloadable/viewable in-app.
- **On-Demand Summaries:**  
  - “Summarize My Data” button in each module and globally.
- **No Uploading of Past Logs:**  
  - Only download/export; all logging in-app.
- **Past Logs:**  
  - Not editable in MVP.

---

## 5. Security & Environment

- **Password Authentication:**  
  - Simple password for MVP.
- **Environment Variables:**  
  - Use `.env` or `.streamlit/secrets.toml` for secrets (API keys, passwords).
- **Replit/GitHub Compatibility:**  
  - `.replit` tracked by git for Replit deployment.
  - `.gitignore` excludes sensitive files and local caches.
  - `requirements.txt` lists all dependencies.
  - `README.md` with setup, usage, and deployment instructions.
  - `LICENSE` for open source/commercial use as needed.

---

## 6. Replit Deployment Guide

- **Project Structure:**  
  - All core modules and utilities in dedicated folders.
  - Place `.replit` file at root. Example:
    ```
    run = "streamlit run app.py"
    ```
  - Ensure `requirements.txt` includes all Python dependencies (e.g., `streamlit`, `openai`, `tesserocr`, etc.).
  - Use `.env` or `.streamlit/secrets.toml` for API keys and secrets.  
    - On Replit, set secrets via the "Secrets" tab (not in code).
  - Add `.replit` and `README.md` to git for Replit compatibility.

- **GitHub Sync:**  
  - Initialize git repo, commit all files except those in `.gitignore`.
  - Push to GitHub for version control and collaboration.
  - Replit can import directly from GitHub for cloud prototyping.

- **Streamlit Tips for Replit:**  
  - Use `st.sidebar` for sidebar navigation.
  - Use `st.session_state` for conversational flows and log persistence.
  - For file exports, use `st.download_button`.
  - For image/OCR, use `st.file_uploader` and `tesserocr` or similar.
  - For scheduling (summaries), use background tasks or prompt user to run summary on schedule (Replit has limitations on persistent background jobs).

- **Security:**  
  - Never commit secrets to git.
  - Use Replit's secrets management for API keys, passwords, etc.

---

## 7. Planned Extensibility

- AI/analytics, multi-user support, module expansion, API integrations, and more.

---

## 8. Open Questions / Future Considerations

- Integration with financial APIs (Plaid, Yodlee, etc.).
- Deeper behavioral finance research.
- Strategic partnerships and B2C scaling.

---

**Please review and edit this file as needed before implementation. Once confirmed, this will serve as the blueprint for LatticeFlow and Replit deployment.**
