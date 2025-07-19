# Pre/Post Workout Scoring Frameworks
# Energy: 1 = depleted, 5 = functional but tired, 10 = fully energized
# Mood: 1 = anxious/irritable, 5 = neutral, 10 = positive/uplifted
# Recovery: 1 = sore/exhausted, 5 = okay, 10 = fully recovered

import streamlit as st
import json
from datetime import datetime

# --- Constants and Filepaths ---
WORKOUT_PLAN_PATH = "kinetica-forge/workout_plan.json"
WORKOUT_HISTORY_PATH = "kinetica-forge/workout_history.json"
PHYSIO_LOG_PATH = "kinetica-forge/physio_log.json"

# --- Utility Functions ---
def load_workout_plan():
    with open(WORKOUT_PLAN_PATH) as f:
        return json.load(f)

def save_workout_history(entry):
    try:
        with open(WORKOUT_HISTORY_PATH, "r+") as f:
            data = json.load(f)
            today = datetime.now().strftime("%Y-%m-%d")
            if today not in data:
                data[today] = []
            data[today].append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        with open(WORKOUT_HISTORY_PATH, "w") as f:
            today = datetime.now().strftime("%Y-%m-%d")
            json.dump({today: [entry]}, f, indent=2)

def save_physio_log(note, tags):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "note": note,
        "tags": tags,
    }
    try:
        with open(PHYSIO_LOG_PATH, "r+") as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        with open(PHYSIO_LOG_PATH, "w") as f:
            json.dump([log_entry], f, indent=2)

# --- Streamlit UI Routines ---
def show_landing_page():
    st.title("Physical Maintenance: Workout Tracking")
    st.write("Select a workout template or start a new workout.")
    plan = load_workout_plan()
    for day, details in plan.items():
        st.subheader(f"{day.title()}: {details['title']}")
        st.write("Mobility:")
        for move in details.get("mobility", []):
            st.write(f"- {move['name']} ({move.get('reps', move.get('duration', ''))})")
        if st.button(f"Start {day.title()} Workout"):
            st.session_state['workout_day'] = day
            st.session_state['page'] = 'log_workout'
    if st.button("+ New Workout"):
        st.session_state['page'] = 'new_workout'

# --- Logging Routine ---
def log_workout_flow(day):
    plan = load_workout_plan()
    details = plan[day]
    st.header(f"Logging: {details['title']}")
    # --- Last Week's Performance ---
    import os
    from datetime import datetime, timedelta
    history_path = WORKOUT_HISTORY_PATH
    # Find most recent previous log for this workout day (e.g., 'friday')
    last_log = None
    last_log_date = None
    if os.path.exists(history_path):
        with open(history_path) as f:
            try:
                history = json.load(f)
                # Get all dates before today, sorted descending
                today_str = datetime.now().strftime("%Y-%m-%d")
                prev_dates = [d for d in history if d < today_str]
                prev_dates.sort(reverse=True)
                for d in prev_dates:
                    for log in history[d]:
                        if log.get("day") == day:
                            last_log = log
                            last_log_date = d
                            break
                    if last_log:
                        break
            except Exception:
                last_log = None
                last_log_date = None
    with st.expander("Last Logged Performance", expanded=True):
        if last_log:
            st.markdown(f"**Date:** {last_log_date}")
            for s in last_log.get("supersets", []):
                st.write(f"- {s['exercise']}: {s['reps']} ({'✔️' if s['completed'] else '❌'})")
            st.write(f"**RPE:** {last_log.get('rpe','')}")
            st.write(f"**Notes:** {last_log.get('notes','')}")
        else:
            st.info(f"No previous log found for this workout.")
    st.write("### Pre-Workout Scores")
    pre_energy = st.slider("Energy (1-10)", 1, 10, 5)
    pre_mood = st.slider("Mood (1-10)", 1, 10, 5)
    pre_recovery = st.slider("Recovery (1-10)", 1, 10, 5)

    st.write("### Warm-up")
    for move in details.get("mobility", []):
        st.checkbox(f"{move['name']} ({move.get('reps', move.get('duration', '') )})", key=f"warmup_{move['name']}")

    st.write("### Supersets")
    superset_logs = []
    for idx, superset in enumerate(details.get("supersets", [])):
        st.subheader(superset["title"])
        for ex in superset["exercises"]:
            reps = st.text_input(f"{ex['name']} reps", value=ex["reps"], key=f"reps_{day}_{idx}_{ex['name']}")
            completed = st.checkbox(f"Completed {ex['name']}", key=f"done_{day}_{idx}_{ex['name']}")
            # Inline suggestion placeholder
            st.caption(ex.get("desc", ""))
            superset_logs.append({"exercise": ex["name"], "reps": reps, "completed": completed})

    st.write("### RPE (Rate of Perceived Exertion)")
    rpe = st.slider("RPE (1-10)", 1, 10, 7)
    st.sidebar.header("RPE Suggestions")
    st.sidebar.write("6 = Easy, 8 = Challenging, 10 = Max effort")

    st.write("### Cool-down")
    st.text_area("Cool-down Notes", key="cooldown_notes")

    st.write("### Post-Workout Scores")
    post_energy = st.slider("Post-Workout Energy (1-10)", 1, 10, 5)
    post_mood = st.slider("Post-Workout Mood (1-10)", 1, 10, 5)
    post_recovery = st.slider("Post-Workout Recovery (1-10)", 1, 10, 5)

    st.write("### Notes & Tags")
    notes = st.text_area("Any notes you'd like to remember?")
    # Auto-tagging stub (to be replaced with GPT integration)
    tags = ["#goal_hit", "#consistency"] if st.checkbox("Tag: Goal Hit") else []

    if st.button("Save Workout Log"):
        entry = {
            "day": day,
            "timestamp": datetime.now().isoformat(),
            "pre_scores": {"energy": pre_energy, "mood": pre_mood, "recovery": pre_recovery},
            "supersets": superset_logs,
            "rpe": rpe,
            "post_scores": {"energy": post_energy, "mood": post_mood, "recovery": post_recovery},
            "notes": notes,
            "tags": tags
        }
        save_workout_history(entry)
        st.success("Workout log saved!")
        st.session_state['page'] = 'landing'

    if st.button("Export to Markdown/JSON"):
        st.download_button("Download JSON", json.dumps(entry, indent=2), file_name="workout_log.json")
        st.download_button("Download Markdown", export_markdown(entry), file_name="workout_log.md")

# --- Physio/Doctor/Chiro Log ---
def physio_log_flow():
    st.header("Physio/Doctor/Chiro Log")
    note = st.text_area("Enter note:")
    tags = st.text_input("Tags (comma-separated):")
    if st.button("Save Note"):
        save_physio_log(note, [t.strip() for t in tags.split(",") if t.strip()])
        st.success("Note saved!")

# --- Export Utilities ---
def export_markdown(entry):
    md = f"## 🏋️ Workout Log — {entry['timestamp'][:10]}\n"
    md += f"### Pre-Workout\nEnergy: {entry['pre_scores']['energy']}\nMood: {entry['pre_scores']['mood']}\nRecovery: {entry['pre_scores']['recovery']}\n"
    md += "### Supersets\n"
    for s in entry['supersets']:
        md += f"- {s['exercise']}: {s['reps']} reps, Completed: {'Yes' if s['completed'] else 'No'}\n"
    md += f"### RPE: {entry['rpe']}\n"
    md += f"### Post-Workout\nEnergy: {entry['post_scores']['energy']}\nMood: {entry['post_scores']['mood']}\nRecovery: {entry['post_scores']['recovery']}\n"
    md += f"### Notes\n{entry['notes']}\n"
    md += f"### Tags\n{' '.join(entry['tags'])}\n"
    return md

# --- Main Entrypoint ---
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'landing'
    if st.session_state['page'] == 'landing':
        show_landing_page()
    elif st.session_state['page'] == 'log_workout':
        log_workout_flow(st.session_state['workout_day'])
    elif st.session_state['page'] == 'new_workout':
        new_workout_flow()
    elif st.session_state['page'] == 'physio_log':
        physio_log_flow()

# --- OCR Integration Placeholder ---
def ocr_upload_placeholder():
    st.write("OCR upload and parsing coming soon.")

# Only run main if this is the main module
if __name__ == "__main__":
    main()
