
import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import sys

# Module imports will be handled when backend is ready
# For now, using placeholder functions to scaffold UI

# --- Configuration ---
st.set_page_config(
    page_title="LatticeFlow",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize session state ---
def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 'AM Journal'
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = {}
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = load_user_preferences()
    if 'workout_page' not in st.session_state:
        st.session_state.workout_page = 'landing'
    if 'journal_page' not in st.session_state:
        st.session_state.journal_page = 'start'
    if 'am_data' not in st.session_state:
        st.session_state.am_data = {}
    if 'pm_data' not in st.session_state:
        st.session_state.pm_data = {}

# --- Utility functions ---
def load_user_preferences() -> Dict[str, Any]:
    """Load user preferences from file or return defaults"""
    try:
        if os.path.exists('user_preferences.json'):
            with open('user_preferences.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading preferences: {e}")
    
    return {
        'theme': 'light',
        'api_keys': {},
        'default_metrics': {}
    }

def save_user_preferences(preferences: Dict[str, Any]):
    """Save user preferences to file"""
    try:
        with open('user_preferences.json', 'w') as f:
            json.dump(preferences, f, indent=2)
    except Exception as e:
        st.error(f"Error saving preferences: {e}")

def get_secret(key: str) -> Optional[str]:
    """Get secret from Streamlit secrets or environment"""
    try:
        return st.secrets.get(key) or os.getenv(key)
    except Exception:
        return None

# --- Simplified authentication (no password for testing) ---
def authenticate():
    """Skip authentication for testing"""
    st.session_state.authenticated = True
    st.sidebar.title("🌊 LatticeFlow")
    st.sidebar.markdown("---")
    st.sidebar.info("🔓 Authentication disabled for testing")

# --- Enhanced navigation ---
def sidebar_navigation():
    """Enhanced sidebar navigation with icons and organization"""
    # Collapsible sidebar toggle
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state.sidebar_collapsed = False
    
    # Toggle button in main area
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("☰" if st.session_state.sidebar_collapsed else "✕", key="sidebar_toggle"):
            st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
            st.rerun()
    
    if not st.session_state.sidebar_collapsed:
        st.sidebar.markdown("## 📱 Navigation")
        
        # Group sections logically
        sections = {
            "📝 Journaling": ["AM Journal", "PM Journal"],
            "💪 Physical": ["Workout Tracker", "Macro Cheat Sheet"],
            "🧠 Mental Tools": ["Memory Board", "ADHD Toolkit"],
            "⚙️ System": ["Diagnostics", "Settings"]
        }
        
        selected_section = st.session_state.current_section
        
        for category, items in sections.items():
            st.sidebar.markdown(f"**{category}**")
            for item in items:
                if st.sidebar.button(item, key=f"nav_{item}"):
                    st.session_state.current_section = item
                    # Reset journal pages when switching sections
                    if item in ["AM Journal", "PM Journal"]:
                        st.session_state.journal_page = 'start'
                    st.rerun()
        
        # Add logout button
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    return st.session_state.current_section

# --- Enhanced placeholder functions ---
def am_journal():
    """AM Journal with Next button flow"""
    st.header("🌅 AM Journal")
    
    # Load instruction engine
    try:
        with open('aether-core/instruction_engine.json', 'r') as f:
            instructions = json.load(f)
    except FileNotFoundError:
        st.error("Instruction engine not found. Please ensure aether-core/instruction_engine.json exists.")
        return
    
    if st.session_state.journal_page == 'start':
        st.info("Begin your morning routine with a centering moment.")
        
        if st.button("Start Morning Routine", key="start_am"):
            st.session_state.journal_page = 'mantra'
            st.rerun()
    
    elif st.session_state.journal_page == 'mantra':
        st.markdown("### 🧘 Mantra")
        st.markdown("#### *I choose commitment, integrity, control, and compassion for the best version of myself.*")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start 1-Minute Pause", key="am_pause"):
                st.info("Take a full minute to center yourself...")
                # In a real implementation, this would pause for 60 seconds
        with col2:
            pause_complete = st.checkbox("Pause Complete")
        
        if st.button("Next: Sleep & Energy →", key="am_next1"):
            st.session_state.am_data['pause_complete'] = pause_complete
            st.session_state.journal_page = 'sleep_energy'
            st.rerun()
    
    elif st.session_state.journal_page == 'sleep_energy':
        st.markdown("### 😴 Sleep & Energy Assessment")
        st.caption("Sleep Scoring (1–10): 7 hours = 10/10. Halve the score for 3.5 hours. Round based on quality.")
        
        col1, col2 = st.columns(2)
        with col1:
            sleep_hours = st.number_input("Hours of sleep:", min_value=0.0, max_value=12.0, 
                                        value=st.session_state.am_data.get('sleep_hours', 7.0), step=0.5)
            sleep_quality = st.slider("Sleep Quality (1–10)", 1, 10, 
                                    st.session_state.am_data.get('sleep_quality', 5),
                                    help="1 = very poor (<4h), 5 = light/interrupted, 10 = rested/uninterrupted")
        with col2:
            energy_score = st.slider("Energy Level (1–10)", 1, 10, 
                                   st.session_state.am_data.get('energy_score', 5),
                                   help="1 = depleted, 5 = functional but tired, 10 = energized and clear")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="am_back1"):
                st.session_state.journal_page = 'mantra'
                st.rerun()
        with col2:
            if st.button("Next: ADHD Focus →", key="am_next2"):
                st.session_state.am_data.update({
                    'sleep_hours': sleep_hours,
                    'sleep_quality': sleep_quality,
                    'energy_score': energy_score
                })
                st.session_state.journal_page = 'adhd_focus'
                st.rerun()
    
    elif st.session_state.journal_page == 'adhd_focus':
        st.markdown("### 🎯 ADHD Focus Planning")
        adhd_plan = st.text_area("What is your ADHD focus for today?", height=100,
                                value=st.session_state.am_data.get('adhd_plan', ''))
        strategy = st.text_area("What strategy will support this?", height=100,
                               value=st.session_state.am_data.get('strategy', ''))
        success = st.text_area("What would make today feel like a success?", height=100,
                              value=st.session_state.am_data.get('success', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="am_back2"):
                st.session_state.journal_page = 'sleep_energy'
                st.rerun()
        with col2:
            if st.button("Next: Relational →", key="am_next3"):
                st.session_state.am_data.update({
                    'adhd_plan': adhd_plan,
                    'strategy': strategy,
                    'success': success
                })
                st.session_state.journal_page = 'relational'
                st.rerun()
    
    elif st.session_state.journal_page == 'relational':
        st.markdown("### ❤️ Relational Intentions")
        
        col1, col2 = st.columns(2)
        with col1:
            gabby_intention = st.text_area("How do you want to show up for Gabby today?", height=80,
                                         value=st.session_state.am_data.get('intentions', {}).get('Gabby', ''))
            cleo_intention = st.text_area("What is your intention for Cleo today?", height=80,
                                        value=st.session_state.am_data.get('intentions', {}).get('Cleo', ''))
        
        with col2:
            parents_intention = st.text_area("Any follow-up needed for your parents or brother today?", height=80,
                                           value=st.session_state.am_data.get('intentions', {}).get('Parents/Brother', ''))
            friends_intention = st.text_area("How might you reach out to friends today?", height=80,
                                           value=st.session_state.am_data.get('intentions', {}).get('Friends', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="am_back3"):
                st.session_state.journal_page = 'adhd_focus'
                st.rerun()
        with col2:
            if st.button("Save & Complete →", key="am_save"):
                intentions = {
                    'Gabby': gabby_intention,
                    'Cleo': cleo_intention,
                    'Parents/Brother': parents_intention,
                    'Friends': friends_intention
                }
                st.session_state.am_data['intentions'] = intentions
                
                # Save AM Log
                am_entry = {
                    "timestamp": datetime.now().isoformat(),
                    **st.session_state.am_data
                }
                
                # Save to file
                os.makedirs("vesper-archive", exist_ok=True)
                with open(f"vesper-archive/am_log_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
                    json.dump(am_entry, f, indent=2)
                
                st.success("✅ Morning reflection saved!")
                st.balloons()
                st.session_state.journal_page = 'complete'
                st.rerun()
    
    elif st.session_state.journal_page == 'complete':
        st.success("🎉 Morning routine complete!")
        st.info("Your morning reflection has been saved. Have a great day!")
        
        if st.button("Start New Morning Routine", key="am_restart"):
            st.session_state.journal_page = 'start'
            st.session_state.am_data = {}
            st.rerun()

def pm_journal():
    """PM Journal with Next button flow"""
    st.header("🌙 PM Journal")
    
    # Load instruction engine and metric groups
    try:
        with open('aether-core/instruction_engine.json', 'r') as f:
            instructions = json.load(f)
        with open('numina-vault/metric_groups.json', 'r') as f:
            metric_groups = json.load(f)
    except FileNotFoundError:
        st.error("Required files not found. Please ensure aether-core/instruction_engine.json and numina-vault/metric_groups.json exist.")
        return
    
    if st.session_state.journal_page == 'start':
        st.info("Begin your evening reflection with a centering moment.")
        
        if st.button("Start Evening Routine", key="start_pm"):
            st.session_state.journal_page = 'mantra'
            st.rerun()
    
    elif st.session_state.journal_page == 'mantra':
        st.markdown("### 🧘 Mantra")
        st.markdown("#### *I choose commitment, integrity, control, and compassion for the best version of myself.*")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start 1-Minute Pause", key="pm_pause"):
                st.info("Take a full minute to center yourself...")
        with col2:
            pause_complete = st.checkbox("Pause Complete")
        
        if st.button("Next: Reflection →", key="pm_next1"):
            st.session_state.pm_data['pause_complete'] = pause_complete
            st.session_state.journal_page = 'reflection'
            st.rerun()
    
    elif st.session_state.journal_page == 'reflection':
        st.markdown("### 💭 Free-Form Reflection")
        st.info("Start with completely free-form reflection. The system will analyze this for scoring and tagging.")
        
        reflection = st.text_area("Begin your reflection here:", height=200, 
                                 value=st.session_state.pm_data.get('reflection', ''),
                                 placeholder="Share freely about your day, feelings, relationships, challenges, wins...")
        
        reflection_complete = st.checkbox("Free reflection complete", 
                                        value=st.session_state.pm_data.get('reflection_complete', False))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="pm_back1"):
                st.session_state.journal_page = 'mantra'
                st.rerun()
        with col2:
            if st.button("Next: Metrics →", key="pm_next2"):
                st.session_state.pm_data.update({
                    'reflection': reflection,
                    'reflection_complete': reflection_complete
                })
                st.session_state.journal_page = 'metrics'
                st.rerun()
    
    elif st.session_state.journal_page == 'metrics':
        if st.session_state.pm_data.get('reflection_complete') and st.session_state.pm_data.get('reflection', '').strip():
            st.markdown("### 📊 Metric Scoring")
            st.info("Based on your reflection, here are proposed metric scores:")
            
            scores = st.session_state.pm_data.get('scores', {})
            for group_name, group_metrics in metric_groups["metric_groups"].items():
                if group_name in ["Emotional Regulation", "ADHD + Self-Management", "Relationships", "Wellness + Physical State", "Learning + Meaning"]:
                    st.subheader(f"{group_name}")
                    for metric_name, metric_info in group_metrics.items():
                        if metric_info["scale"] == "1–10":
                            scores[metric_name] = st.slider(f"{metric_name}", 1, 10, 
                                                           scores.get(metric_name, 5),
                                                           help=metric_info["definition"])
                        else:  # Y/N
                            scores[metric_name] = st.selectbox(f"{metric_name}", ["Y", "N"], 
                                                              index=0 if scores.get(metric_name, "Y") == "Y" else 1,
                                                              help=metric_info["definition"])
            
            # Relationship follow-ups
            st.markdown("### 👥 Relationship Follow-ups")
            relationships = ["Gabby", "Cleo", "Parents", "Brother", "Friends"]
            relationship_notes = st.session_state.pm_data.get('relationship_notes', {})
            
            for person in relationships:
                if person.lower() not in st.session_state.pm_data.get('reflection', '').lower():
                    relationship_notes[person] = st.text_area(f"Add note about {person}:", height=80,
                                                            value=relationship_notes.get(person, ''))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back", key="pm_back2"):
                    st.session_state.journal_page = 'reflection'
                    st.rerun()
            with col2:
                if st.button("Next: Summary →", key="pm_next3"):
                    st.session_state.pm_data.update({
                        'scores': scores,
                        'relationship_notes': relationship_notes
                    })
                    st.session_state.journal_page = 'summary'
                    st.rerun()
        else:
            st.info("Complete your reflection in the previous step to proceed with scoring.")
            if st.button("← Back to Reflection", key="pm_back2_alt"):
                st.session_state.journal_page = 'reflection'
                st.rerun()
    
    elif st.session_state.journal_page == 'summary':
        st.markdown("### 🏷️ Tags & Emotions")
        st.info("GPT will analyze your reflection for emotional tags and themes.")
        
        # Placeholder for GPT-generated tags
        suggested_tags = ["#reflection", "#daily_review"]  # This would come from GPT
        selected_tags = st.multiselect("Review and select tags:", suggested_tags, 
                                     default=st.session_state.pm_data.get('tags', suggested_tags))
        
        # Macro summary
        st.markdown("### 🍎 Macro Summary")
        macro_summary = st.text_input("Quick macro summary for today:", 
                                     value=st.session_state.pm_data.get('macro_summary', ''),
                                     placeholder="e.g., 2000 cal, 120g protein")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="pm_back3"):
                st.session_state.journal_page = 'metrics'
                st.rerun()
        with col2:
            if st.button("Save & Complete →", key="pm_save"):
                st.session_state.pm_data.update({
                    'tags': selected_tags,
                    'macro_summary': macro_summary
                })
                
                # Save PM Log
                pm_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "reflection": st.session_state.pm_data.get('reflection', ''),
                    "scores": st.session_state.pm_data.get('scores', {}),
                    "relationship_notes": st.session_state.pm_data.get('relationship_notes', {}),
                    "tags": selected_tags,
                    "macro_summary": macro_summary,
                    "gpt_analysis": "GPT analysis will be added here"
                }
                
                # Save to file
                os.makedirs("vesper-archive", exist_ok=True)
                with open(f"vesper-archive/pm_log_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
                    json.dump(pm_entry, f, indent=2)
                
                st.success("✅ Evening reflection saved!")
                st.balloons()
                st.session_state.journal_page = 'complete'
                st.rerun()
    
    elif st.session_state.journal_page == 'complete':
        st.success("🎉 Evening routine complete!")
        st.info("Your evening reflection has been saved. Sweet dreams!")
        
        if st.button("Start New Evening Routine", key="pm_restart"):
            st.session_state.journal_page = 'start'
            st.session_state.pm_data = {}
            st.rerun()

def workout_tracker():
    """Workout tracking with improved navigation and per-exercise RPE"""
    st.header("💪 Workout Tracker")
    
    # Load workout plan
    try:
        with open('kinetica-forge/workout_plan.json', 'r') as f:
            workout_plan = json.load(f)
    except FileNotFoundError:
        st.error("Workout plan not found. Please ensure kinetica-forge/workout_plan.json exists.")
        return
    
    # RPE Framework in sidebar
    with st.sidebar:
        st.markdown("### 📊 RPE Framework")
        st.markdown("""
        **1-2**: Very light activity
        **3-4**: Light activity
        **5-6**: Moderate activity
        **7**: Vigorous activity
        **8**: Very vigorous activity
        **9**: Extremely vigorous
        **10**: Maximum effort
        """)
    
    if st.session_state.workout_page == 'landing':
        st.info("Select a workout template from your established plan:")
        
        # Show workout options
        for day, details in workout_plan.items():
            st.subheader(f"{day.title()}: {details['title']}")
            
            # Show mobility warm-up
            with st.expander("Mobility Warm-up"):
                for move in details.get("mobility", []):
                    st.write(f"• {move['name']} ({move.get('reps', move.get('duration', ''))})")
            
            # Show supersets preview
            with st.expander("Supersets Preview"):
                for superset in details.get("supersets", []):
                    st.write(f"**{superset['title']}** - {superset.get('sets', 4)} sets")
                    for ex in superset["exercises"]:
                        st.write(f"  • {ex['name']} - {ex['reps']}")
            
            if st.button(f"Start {day.title()} Workout", key=f"start_{day}"):
                st.session_state.workout_day = day
                st.session_state.workout_page = 'logging'
                st.rerun()
        
        # Custom workout option
        if st.button("+ Create Custom Workout"):
            st.session_state.workout_page = 'custom'
            st.rerun()
    
    elif st.session_state.workout_page == 'logging':
        workout_day = st.session_state.workout_day
        details = workout_plan[workout_day]
        
        st.subheader(f"Logging: {details['title']}")
        
        # Back button
        if st.button("← Back to Workout Selection"):
            st.session_state.workout_page = 'landing'
            st.rerun()
        
        # Pre-workout scoring with info buttons
        st.markdown("### 🔄 Pre-Workout Assessment")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Energy Framework**\n1 = depleted\n5 = functional but tired\n10 = fully energized")
            pre_energy = st.slider("Energy (1-10)", 1, 10, 5, key="pre_energy")
        with col2:
            st.info("**Mood Framework**\n1 = anxious/irritable\n5 = neutral\n10 = positive/uplifted")
            pre_mood = st.slider("Mood (1-10)", 1, 10, 5, key="pre_mood")
        with col3:
            st.info("**Recovery Framework**\n1 = sore/exhausted\n5 = okay\n10 = fully recovered")
            pre_recovery = st.slider("Recovery (1-10)", 1, 10, 5, key="pre_recovery")
        
        # Warm-up tracking
        st.markdown("### 🤸 Warm-up")
        warmup_completed = {}
        for move in details.get("mobility", []):
            warmup_completed[move['name']] = st.checkbox(
                f"{move['name']} ({move.get('reps', move.get('duration', ''))})",
                key=f"warmup_{move['name']}"
            )
        
        # Superset logging with per-exercise RPE
        st.markdown("### 🏋️ Supersets")
        superset_logs = []
        
        for superset_idx, superset in enumerate(details.get("supersets", [])):
            st.subheader(f"{superset['title']} - {superset.get('sets', 4)} sets")
            
            for ex_idx, ex in enumerate(superset["exercises"]):
                st.markdown(f"**{ex['name']}** - {ex['reps']}")
                if ex.get("desc"):
                    st.caption(ex["desc"])
                
                # Create columns for each set
                set_cols = st.columns(superset.get('sets', 4))
                exercise_sets = []
                
                for set_num in range(superset.get('sets', 4)):
                    with set_cols[set_num]:
                        st.write(f"Set {set_num + 1}")
                        actual_reps = st.text_input(
                            "Reps", 
                            value=ex["reps"], 
                            key=f"reps_{superset_idx}_{ex_idx}_{set_num}"
                        )
                        rpe = st.slider(
                            "RPE", 
                            1, 10, 7, 
                            key=f"rpe_{superset_idx}_{ex_idx}_{set_num}"
                        )
                        completed = st.checkbox(
                            "✓", 
                            key=f"done_{superset_idx}_{ex_idx}_{set_num}"
                        )
                        
                        exercise_sets.append({
                            "set": set_num + 1,
                            "reps": actual_reps,
                            "rpe": rpe,
                            "completed": completed
                        })
                
                superset_logs.append({
                    "exercise": ex["name"],
                    "planned_reps": ex["reps"],
                    "sets": exercise_sets
                })
                
                st.markdown("---")
        
        # Cool-down
        st.markdown("### 🧘 Cool-down")
        cooldown_notes = st.text_area("Cool-down notes:", height=80)
        
        # Post-workout scoring with info buttons
        st.markdown("### 🔄 Post-Workout Assessment")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Energy Framework**\n1 = depleted\n5 = functional but tired\n10 = fully energized")
            post_energy = st.slider("Post-Energy (1-10)", 1, 10, 5, key="post_energy")
        with col2:
            st.info("**Mood Framework**\n1 = anxious/irritable\n5 = neutral\n10 = positive/uplifted")
            post_mood = st.slider("Post-Mood (1-10)", 1, 10, 5, key="post_mood")
        with col3:
            st.info("**Recovery Framework**\n1 = sore/exhausted\n5 = okay\n10 = fully recovered")
            post_recovery = st.slider("Post-Recovery (1-10)", 1, 10, 5, key="post_recovery")
        
        # Notes and auto-tagging
        st.markdown("### 📝 Notes & Tags")
        workout_notes = st.text_area("Workout notes:", height=100)
        
        # Auto-generated tags
        completed_sets = sum(1 for log in superset_logs for s in log["sets"] if s["completed"])
        total_sets = sum(len(log["sets"]) for log in superset_logs)
        
        auto_tags = []
        if completed_sets > total_sets * 0.8:
            auto_tags.append("#goal_hit")
        avg_rpe = sum(s["rpe"] for log in superset_logs for s in log["sets"]) / max(total_sets, 1)
        if avg_rpe >= 8:
            auto_tags.append("#high_intensity")
        auto_tags.append("#consistency")
        
        selected_tags = st.multiselect("Tags:", auto_tags, default=auto_tags)
        
        # Save workout
        if st.button("💾 Save Workout Log"):
            workout_entry = {
                "day": workout_day,
                "title": details['title'],
                "timestamp": datetime.now().isoformat(),
                "pre_scores": {"energy": pre_energy, "mood": pre_mood, "recovery": pre_recovery},
                "warmup_completed": warmup_completed,
                "supersets": superset_logs,
                "cooldown_notes": cooldown_notes,
                "post_scores": {"energy": post_energy, "mood": post_mood, "recovery": post_recovery},
                "notes": workout_notes,
                "tags": selected_tags
            }
            
            # Save to workout history
            os.makedirs("kinetica-forge", exist_ok=True)
            try:
                with open("kinetica-forge/workout_history.json", "r") as f:
                    history = json.load(f)
            except FileNotFoundError:
                history = {}
            
            today = datetime.now().strftime("%Y-%m-%d")
            if today not in history:
                history[today] = []
            history[today].append(workout_entry)
            
            with open("kinetica-forge/workout_history.json", "w") as f:
                json.dump(history, f, indent=2)
            
            st.success("✅ Workout logged successfully!")
            st.balloons()
            
            # Export options
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "Download JSON",
                    json.dumps(workout_entry, indent=2),
                    file_name=f"workout_log_{today}.json",
                    mime="application/json"
                )
            with col2:
                # Generate markdown export
                markdown_content = generate_workout_markdown(workout_entry)
                st.download_button(
                    "Download Markdown",
                    markdown_content,
                    file_name=f"workout_log_{today}.md",
                    mime="text/markdown"
                )
    
    elif st.session_state.workout_page == 'custom':
        st.subheader("Custom Workout (Coming Soon)")
        st.info("Custom workout creation will be implemented here")
        
        if st.button("← Back to Workout Selection"):
            st.session_state.workout_page = 'landing'
            st.rerun()

def generate_workout_markdown(entry):
    """Generate markdown export for workout"""
    md = f"## 🏋️ Workout Log — {entry['timestamp'][:10]}\n\n"
    md += f"### {entry['title']}\n\n"
    md += f"### 🔄 Pre-Workout\n"
    md += f"- Energy: {entry['pre_scores']['energy']}/10\n"
    md += f"- Mood: {entry['pre_scores']['mood']}/10\n"
    md += f"- Recovery: {entry['pre_scores']['recovery']}/10\n\n"
    
    md += f"### 🏋️ Supersets\n"
    for s in entry['supersets']:
        md += f"**{s['exercise']}**\n"
        for set_data in s['sets']:
            status = "✅" if set_data['completed'] else "❌"
            md += f"- {status} Set {set_data['set']}: {set_data['reps']} reps @ RPE {set_data['rpe']}\n"
        md += "\n"
    
    md += f"### 🔄 Post-Workout\n"
    md += f"- Energy: {entry['post_scores']['energy']}/10\n"
    md += f"- Mood: {entry['post_scores']['mood']}/10\n"
    md += f"- Recovery: {entry['post_scores']['recovery']}/10\n\n"
    
    md += f"### 📝 Notes\n{entry['notes']}\n\n"
    md += f"### 🏷️ Tags\n{' '.join(entry['tags'])}\n"
    
    return md

def macro_cheat_sheet():
    """Macro tracking with mobile-optimized OCR support"""
    st.header("🍎 Macro Cheat Sheet")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Quick Reference", "📱 Label Scanner", "🛒 Grocery List", "📖 Meal Planning"])
    
    with tab1:
        st.info("Quick macro reference for common foods.")
        
        # Common foods reference
        common_foods = {
            "Protein": {"Chicken breast (100g)": "23g protein, 165 cal", "Eggs (1 large)": "6g protein, 70 cal"},
            "Carbs": {"Rice (100g cooked)": "23g carbs, 130 cal", "Oats (50g dry)": "27g carbs, 190 cal"},
            "Fats": {"Olive oil (1 tbsp)": "14g fat, 120 cal", "Avocado (100g)": "15g fat, 160 cal"}
        }
        
        for category, foods in common_foods.items():
            st.subheader(category)
            for food, macro in foods.items():
                st.write(f"• **{food}**: {macro}")
    
    with tab2:
        st.info("📱 Scan food labels for macro information")
        
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader("Upload food label image", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                st.image(uploaded_file, caption="Uploaded label")
                st.info("OCR processing will be implemented here")
        
        with col2:
            st.markdown("### 📸 Mobile Camera")
            if st.button("📸 Take Photo", help="Use camera to scan label"):
                st.info("Camera integration will be implemented here")
    
    with tab3:
        st.info("🛒 Track grocery items and shopping lists")
        
        col1, col2 = st.columns(2)
        with col1:
            uploaded_grocery = st.file_uploader("Upload grocery receipt", type=['png', 'jpg', 'jpeg'])
            if uploaded_grocery:
                st.image(uploaded_grocery, caption="Grocery receipt")
                st.info("Receipt OCR processing will be implemented here")
        
        with col2:
            st.markdown("### 📸 Snap Receipt")
            if st.button("📸 Photo Receipt", help="Use camera to scan receipt"):
                st.info("Receipt camera integration will be implemented here")
        
        # Manual grocery list
        st.markdown("### Manual Grocery List")
        grocery_item = st.text_input("Add grocery item:")
        if st.button("Add Item") and grocery_item:
            if 'grocery_list' not in st.session_state:
                st.session_state.grocery_list = []
            st.session_state.grocery_list.append(grocery_item)
            st.success(f"Added: {grocery_item}")
        
        # Display grocery list
        if 'grocery_list' in st.session_state and st.session_state.grocery_list:
            st.markdown("### Current List")
            for i, item in enumerate(st.session_state.grocery_list):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {item}")
                with col2:
                    if st.button("Remove", key=f"remove_grocery_{i}"):
                        st.session_state.grocery_list.pop(i)
                        st.rerun()
    
    with tab4:
        st.info("📖 Upload and catalog recipes and meal ideas")
        
        col1, col2 = st.columns(2)
        with col1:
            recipe_upload = st.file_uploader("Upload recipe image", type=['png', 'jpg', 'jpeg'])
            if recipe_upload:
                st.image(recipe_upload, caption="Recipe")
                st.info("Recipe OCR processing will be implemented here")
        
        with col2:
            st.markdown("### 📸 Photo Recipe")
            if st.button("📸 Take Recipe Photo", help="Use camera to capture recipe"):
                st.info("Recipe camera integration will be implemented here")
        
        # Manual recipe entry
        st.markdown("### Manual Recipe Entry")
        recipe_name = st.text_input("Recipe name:")
        recipe_content = st.text_area("Recipe content:", height=200)
        
        if st.button("Save Recipe") and recipe_name and recipe_content:
            if 'recipes' not in st.session_state:
                st.session_state.recipes = []
            
            new_recipe = {
                'name': recipe_name,
                'content': recipe_content,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.recipes.append(new_recipe)
            st.success(f"Recipe '{recipe_name}' saved!")
        
        # Display recipes
        if 'recipes' in st.session_state and st.session_state.recipes:
            st.markdown("### Saved Recipes")
            for i, recipe in enumerate(st.session_state.recipes):
                with st.expander(f"{recipe['name']} - {recipe['created']}"):
                    st.write(recipe['content'])
                    if st.button("Delete Recipe", key=f"delete_recipe_{i}"):
                        st.session_state.recipes.pop(i)
                        st.rerun()

def memory_board():
    """Card-based memory board"""
    st.header("🧠 Memory Board")
    
    tab1, tab2 = st.tabs(["📝 Active Cards", "➕ Add New"])
    
    with tab1:
        st.info("Your memory cards and reminders.")
        
        # Initialize cards in session state
        if 'memory_cards' not in st.session_state:
            st.session_state.memory_cards = []
        
        # Display cards in grid
        cols = st.columns(3)
        for i, card in enumerate(st.session_state.memory_cards):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"**{card['title']}**")
                    st.write(card['content'])
                    st.caption(f"Created: {card['created']}")
                    if st.button("Remove", key=f"remove_card_{i}"):
                        st.session_state.memory_cards.pop(i)
                        st.rerun()
    
    with tab2:
        st.info("Create new memory cards.")
        
        card_title = st.text_input("Card Title")
        card_content = st.text_area("Card Content")
        card_type = st.selectbox("Card Type", ["Idea", "Reminder", "Script", "Note"])
        
        if st.button("Add Card") and card_title and card_content:
            new_card = {
                'title': card_title,
                'content': card_content,
                'type': card_type,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.memory_cards.append(new_card)
            st.success("Card added!")
            st.rerun()

def adhd_toolkit():
    """ADHD tools and scripts"""
    st.header("🧠 ADHD Toolkit")
    
    tab1, tab2 = st.tabs(["🛠️ Quick Tools", "📜 Scripts"])
    
    with tab1:
        st.info("Quick ADHD management tools.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 Focus Timer")
            timer_minutes = st.slider("Minutes", 5, 60, 25)
            if st.button("Start Timer"):
                st.info(f"Timer started for {timer_minutes} minutes!")
        
        with col2:
            st.subheader("📋 Quick Capture")
            quick_note = st.text_area("Brain dump:", height=100)
            if st.button("Save Note"):
                st.success("Note saved to memory board!")
    
    with tab2:
        st.info("ADHD scripts and coping strategies.")
        
        scripts = [
            {"name": "Morning Routine", "description": "Step-by-step morning routine"},
            {"name": "Task Switching", "description": "Strategies for smooth transitions"},
            {"name": "Emotional Regulation", "description": "Techniques for managing emotions"}
        ]
        
        for script in scripts:
            with st.expander(script["name"]):
                st.write(script["description"])
                st.info("Script content coming soon...")

def diagnostics():
    """System diagnostics and validation"""
    st.header("🔍 Diagnostics & Validation")
    
    tab1, tab2 = st.tabs(["🔧 System Status", "✅ Entry Validation"])
    
    with tab1:
        st.info("System health and configuration check.")
        
        # API key checks
        st.subheader("API Configuration")
        openai_key = get_secret("OPENAI_API_KEY")
        st.write(f"OpenAI API Key: {'✅ Set' if openai_key else '❌ Missing'}")
        
        # File system checks
        st.subheader("File System")
        required_dirs = ['aether-core', 'kinetica-forge', 'arcana-scrolls']
        for dir_name in required_dirs:
            exists = os.path.exists(dir_name)
            st.write(f"{dir_name}: {'✅ Found' if exists else '❌ Missing'}")
    
    with tab2:
        st.info("Validate journal entries and data quality.")
        
        if st.button("Run Validation"):
            st.info("Validation results will appear here...")

def settings():
    """Enhanced settings and configuration"""
    st.header("⚙️ Settings & Configuration")
    
    tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "👤 Preferences", "📖 About"])
    
    with tab1:
        st.info("Configure API keys and external services.")
        st.warning("⚠️ Use the Secrets tab in Replit to set sensitive values securely.")
        
        # Display current secret status
        secrets_to_check = ["OPENAI_API_KEY", "APP_PASSWORD"]
        for secret in secrets_to_check:
            value = get_secret(secret)
            st.write(f"**{secret}**: {'✅ Set' if value else '❌ Not set'}")
    
    with tab2:
        st.info("User preferences and customization.")
        
        # Theme selection
        theme = st.selectbox("Theme", ["Light", "Dark"], 
                           index=0 if st.session_state.user_preferences.get('theme', 'light') == 'light' else 1)
        
        # Save preferences
        if st.button("Save Preferences"):
            st.session_state.user_preferences['theme'] = theme.lower()
            save_user_preferences(st.session_state.user_preferences)
            st.success("Preferences saved!")
    
    with tab3:
        st.info("About LatticeFlow and system information.")
        
        st.markdown("""
        ### 🌊 LatticeFlow
        
        A modular journaling and workout system built with Streamlit.
        
        **Features:**
        - AM/PM journaling with GPT integration
        - Workout tracking with RPE and energy scoring
        - Macro tracking with OCR support
        - ADHD toolkit and memory board
        - Comprehensive diagnostics
        
        **System Specification:**
        - [View README](./README.md)
        - [View Specification](./LATTICEFLOW_SPEC.md)
        """)

# --- Main application ---
def main():
    """Main application entry point"""
    init_session_state()
    authenticate()
    
    # Main content area
    section = sidebar_navigation()
    
    # Route to appropriate section (no LatticeFlow header per request)
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
    
    # Footer
    st.markdown("---")
    st.markdown("*LatticeFlow © 2025 | Built with Streamlit*")

if __name__ == "__main__":
    main()
