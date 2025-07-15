import streamlit as st

# --- Simple password authentication (dummy for now) ---
def authenticate():
    st.sidebar.title("LatticeFlow")
    password = st.sidebar.text_input("Password", type="password")
    if password != "yourpassword":  # TODO: Replace with secure method
        st.sidebar.warning("Enter password to access the app.")
        st.stop()

# --- Navigation ---
def sidebar_navigation():
    st.sidebar.markdown("## Navigation")
    section = st.sidebar.radio(
        "Go to:",
        [
            "AM Journal",
            "PM Journal",
            "Workout Tracker",
            "Macro Cheat Sheet",
            "Memory Board",
            "ADHD Toolkit",
            "Diagnostics",
            "Settings"
        ]
    )
    return section

# --- Placeholder functions for each module ---
def am_journal():
    st.header("AM Journal")
    st.info("Conversational AM journaling UI with GPT scoring, emotion tagging, and metric scales.")
    # TODO: Implement conversational flow, scoring, summaries, emotion tagging, metric anchors
    # TODO: Integrate GPT API for scoring and tagging
    # TODO: Validate entries with runJournalDiagnostics

def pm_journal():
    st.header("PM Journal")
    st.info("Conversational PM journaling UI with GPT scoring, emotion tagging, and metric scales.")
    # TODO: Implement conversational flow, scoring, summaries, emotion tagging, metric anchors
    # TODO: Integrate GPT API for scoring and tagging
    # TODO: Validate entries with runJournalDiagnostics

def workout_tracker():
    st.header("Workout Tracker")
    st.info("Log warm-ups, supersets, RPE, pre/post energy, and view last week's log.")
    # TODO: Implement workout logging, RPE sidebar, pre/post energy scoring
    # TODO: Markdown output for logs
    # TODO: Integrate with macro logs and OCR-ready label scanning

def macro_cheat_sheet():
    st.header("Macro Cheat Sheet")
    st.info("Macro cheat sheet, label scanning (OCR-ready), and grocery tracking.")
    # TODO: Implement macro cheat sheet UI
    # TODO: Add OCR integration for label scanning
    # TODO: Track groceries, compare against standard list

def memory_board():
    st.header("Memory Board")
    st.info("Memory board with cards for ideas, reminders, and AM review scripts.")
    # TODO: Create card-based UI for memory board
    # TODO: Integrate with ADHD scripts and AM review

def adhd_toolkit():
    st.header("ADHD Toolkit")
    st.info("Pop-up tools, scripts, and resources for ADHD management.")
    # TODO: Implement toolkit pop-ups and script integration
    # TODO: Pull scripts into AM review

def diagnostics():
    st.header("Diagnostics & Pre-Log Validator")
    st.info("Pre-log validator for completeness, trends, tagging, structure, reflection depth.")
    # TODO: Implement runJournalDiagnostics
    # TODO: Show diagnostics preview and suggestions

def settings():
    st.header("Settings & About")
    st.markdown("""
    - Configure API keys, secrets, and user preferences.
    - Review project plan and system specification.
    - [View README](./README.md)
    """)
    # TODO: Add forms for secrets and preferences

def main():
    authenticate()
    section = sidebar_navigation()

    st.title("LatticeFlow Modular Journaling & Workout System")
    st.markdown("> **All output and flows must strictly follow the canvas/specification.**")

    if section == "AM Journal":
        am_journal()
    elif section == "PM Journal":
        pm_journal()
    elif section == "Workout Tracker":
        workout_tracker()
    elif section == "Macro Cheat Sheet":
        macro_cheat_sheet()
    elif section == "Memory Board":
        memory_board()
    elif section == "ADHD Toolkit":
        adhd_toolkit()
    elif section == "Diagnostics":
        diagnostics()
    elif section == "Settings":
        settings()
    else:
        st.write("Select a section from the sidebar to get started.")

    # --- Footer ---
    st.markdown("---")
    st.markdown("LatticeFlow &copy; 2025 | [View on GitHub](https://github.com/mehmshah/LatticeFlow)")

if __name__ == "__main__":
    main()