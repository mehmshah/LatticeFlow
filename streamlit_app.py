
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
    initial_sidebar_state="collapsed"
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
    if 'show_landing' not in st.session_state:
        st.session_state.show_landing = True

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
    if not st.session_state.authenticated:
        st.session_state.authenticated = True
        # Show brief auth message in main area
        with st.container():
            st.info("🔓 Authentication disabled for testing")

# --- Enhanced navigation ---
def sidebar_navigation():
    """Right-side hamburger menu navigation with overlay"""
    # Initialize sidebar state
    if 'sidebar_open' not in st.session_state:
        st.session_state.sidebar_open = False
    
    # Create top bar with hamburger menu
    col1, col2 = st.columns([9, 1])
    
    with col2:
        if st.button("☰", key="hamburger_menu", help="Navigation Menu"):
            st.session_state.sidebar_open = not st.session_state.sidebar_open
            st.rerun()
    
    # Show navigation menu when open with overlay styling
    if st.session_state.sidebar_open:
        # Create overlay effect with CSS
        st.markdown("""
        <style>
        .sidebar-overlay {
            position: fixed;
            top: 0;
            right: 0;
            width: 400px;
            height: 100vh;
            background: rgba(255, 255, 255, 0.98);
            border-left: 2px solid #e0e0e0;
            z-index: 1000;
            padding: 20px;
            overflow-y: auto;
            box-shadow: -5px 0 15px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create right-side navigation container
        with st.container():
            st.markdown("---")
            
            # Group sections logically
            sections = {
                "📝 Journaling": ["AM Journal", "PM Journal"],
                "💪 Physical": ["Workout Tracker", "Macro Tracking"],
                "🧠 Mental Tools": ["Memory Board", "ADHD Toolkit"],
                "⚙️ System": ["Diagnostics", "Settings"]
            }
            
            # Create navigation cards
            for category, items in sections.items():
                with st.container():
                    st.markdown(f"### {category}")
                    
                    # Create card-like buttons
                    for item in items:
                        if st.button(
                            item, 
                            key=f"nav_{item}", 
                            use_container_width=True,
                            help=f"Navigate to {item}"
                        ):
                            st.session_state.current_section = item
                            st.session_state.sidebar_open = False
                            st.session_state.show_landing = False
                            # Reset journal pages when switching sections
                            if item in ["AM Journal", "PM Journal"]:
                                st.session_state.journal_page = 'start'
                            st.rerun()
                    
                    st.markdown("")  # Add spacing between categories
            
            # Add special buttons
            st.markdown("---")
            
            # Home button
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.show_landing = True
                st.session_state.sidebar_open = False
                st.rerun()
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
            
            # Close menu button
            if st.button("✕ Close Menu", use_container_width=True):
                st.session_state.sidebar_open = False
                st.rerun()
            
            st.markdown("---")
    
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
                st.session_state.timer_start = datetime.now()
                st.session_state.timer_active = True
                st.session_state.timer_complete = False
                st.rerun()
            
            # Show timer if active
            if st.session_state.get('timer_active', False):
                elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
                remaining = max(0, 60 - elapsed)
                
                if remaining > 0:
                    # Create a live countdown display
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    timer_placeholder = st.empty()
                    timer_placeholder.info(f"⏱️ Centering... {minutes:02d}:{seconds:02d} remaining")
                    
                    # Auto-refresh every second
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.success("✅ Pause complete!")
                    st.session_state.timer_active = False
                    st.session_state.timer_complete = True
        
        with col2:
            pause_complete = st.checkbox("Pause Complete", 
                                       value=st.session_state.get('timer_complete', False))
        
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
            
            # Auto-calculate sleep quality based on 7-hour baseline with proper scaling
            if sleep_hours >= 7:
                auto_quality = 10
            elif sleep_hours >= 6:
                # 6 hours = 85% of 7 hours, scale to 8.5/10
                auto_quality = round((sleep_hours / 7.0) * 10, 1)
            else:
                # Below 6 hours, linear scale down
                auto_quality = max(1, round((sleep_hours / 7.0) * 10))
            
            sleep_quality = st.slider("Sleep Quality (1–10)", 1, 10, 
                                    value=st.session_state.am_data.get('sleep_quality', int(auto_quality)),
                                    help=f"Auto-suggested: {auto_quality}/10 based on {sleep_hours} hours")
            
            # Show percentage and quality calculation
            percentage = round((sleep_hours / 7.0) * 100)
            if sleep_hours == 6:
                st.caption(f"📊 {sleep_hours}h = {percentage}% of baseline → Quality score: 8.5/10")
            else:
                st.caption(f"📊 {sleep_hours}h = {percentage}% of 7-hour baseline")
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
                st.session_state.pm_timer_start = datetime.now()
                st.session_state.pm_timer_active = True
                st.session_state.pm_timer_complete = False
                st.rerun()
            
            # Show timer if active
            if st.session_state.get('pm_timer_active', False):
                elapsed = (datetime.now() - st.session_state.pm_timer_start).total_seconds()
                remaining = max(0, 60 - elapsed)
                
                if remaining > 0:
                    # Create a live countdown display
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    timer_placeholder = st.empty()
                    timer_placeholder.info(f"⏱️ Centering... {minutes:02d}:{seconds:02d} remaining")
                    
                    # Auto-refresh every second
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.success("✅ Pause complete!")
                    st.session_state.pm_timer_active = False
                    st.session_state.pm_timer_complete = True
        
        with col2:
            pause_complete = st.checkbox("Pause Complete", 
                                       value=st.session_state.get('pm_timer_complete', False))
        
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
                if group_name in ["Emotional Regulation", "ADHD + Self-Management", "Relationship", "Wellness + Physical State", "Learning + Meaning"]:
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
    """Workout tracking with improved navigation and sectioned flow"""
    st.header("💪 Workout Tracker")
    
    # Load workout plan
    try:
        with open('kinetica-forge/workout_plan.json', 'r') as f:
            workout_plan = json.load(f)
    except FileNotFoundError:
        st.error("Workout plan not found. Please ensure kinetica-forge/workout_plan.json exists.")
        return
    
    # Initialize workout session state
    if 'workout_section' not in st.session_state:
        st.session_state.workout_section = 'pre_workout'
    if 'workout_data' not in st.session_state:
        st.session_state.workout_data = {}
    
    # RPE Framework info button
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("ℹ️ RPE", help="RPE Framework Reference"):
            with st.expander("📊 RPE Framework", expanded=True):
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
        
        # Show last week's performance if available
        show_weekly_progression()
        
        # Show workout options with complete preview
        for day, details in workout_plan.items():
            st.subheader(f"{day.title()}: {details['title']}")
            
            # Show complete workout preview
            with st.expander("Full Workout Preview"):
                # Warm-up bike
                if 'warmup_bike' in details:
                    bike = details['warmup_bike']
                    st.write(f"**🚴 Warm-up:** {bike['name']} - {bike['duration']} ({bike['intensity']})")
                
                # Mobility
                st.write("**🤸 Mobility:**")
                for move in details.get("mobility", []):
                    st.write(f"• {move['name']} ({move.get('reps', move.get('duration', ''))})")
                
                # Supersets
                st.write("**🏋️ Supersets:**")
                for superset in details.get("supersets", []):
                    st.write(f"**{superset['title']}** - {superset.get('sets', 4)} sets")
                    for ex in superset["exercises"]:
                        st.write(f"  • {ex['name']} - {ex['reps']}")
                
                # Core finisher
                if 'core_finisher' in details:
                    st.write("**💪 Core Finisher:**")
                    for ex in details['core_finisher']:
                        st.write(f"• {ex['name']} - {ex['reps']}")
            
            if st.button(f"Start {day.title()} Workout", key=f"start_{day}"):
                st.session_state.workout_day = day
                st.session_state.workout_page = 'logging'
                st.session_state.workout_section = 'pre_workout'
                st.session_state.workout_data = {}
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
            st.session_state.workout_section = 'pre_workout'
            st.rerun()
        
        # Progress indicator
        sections = ['pre_workout', 'warmup_bike', 'mobility', 'supersets', 'core_finisher', 'post_workout']
        current_idx = sections.index(st.session_state.workout_section)
        progress = (current_idx + 1) / len(sections)
        st.progress(progress, text=f"Section {current_idx + 1} of {len(sections)}")
        
        # Pre-workout section
        if st.session_state.workout_section == 'pre_workout':
            st.markdown("### 🔄 Pre-Workout Assessment")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("**Energy Framework**\n1 = depleted\n5 = functional but tired\n10 = fully energized")
                pre_energy = st.slider("Energy (1-10)", 1, 10, 
                                      st.session_state.workout_data.get('pre_energy', 5), key="pre_energy")
            with col2:
                st.info("**Mood Framework**\n1 = anxious/irritable\n5 = neutral\n10 = positive/uplifted")
                pre_mood = st.slider("Mood (1-10)", 1, 10, 
                                   st.session_state.workout_data.get('pre_mood', 5), key="pre_mood")
            with col3:
                st.info("**Recovery Framework**\n1 = sore/exhausted\n5 = okay\n10 = fully recovered")
                pre_recovery = st.slider("Recovery (1-10)", 1, 10, 
                                        st.session_state.workout_data.get('pre_recovery', 5), key="pre_recovery")
            
            if st.button("Next: Warm-up Bike →"):
                st.session_state.workout_data.update({
                    'pre_energy': pre_energy,
                    'pre_mood': pre_mood,
                    'pre_recovery': pre_recovery
                })
                st.session_state.workout_section = 'warmup_bike'
                st.rerun()
        
        # Warm-up bike section
        elif st.session_state.workout_section == 'warmup_bike':
            st.markdown("### 🚴 Warm-up Bike")
            
            # Bike RPE Framework
            with st.expander("🚴 Bike RPE Framework"):
                st.markdown("""
                **Bike-Specific RPE Scale:**
                - **1-2**: Very easy pedaling, no effort
                - **3-4**: Light effort, can easily hold conversation
                - **5-6**: Moderate effort, slight breathlessness
                - **7**: Vigorous effort, conversation becomes difficult
                - **8**: Very hard effort, short sentences only
                - **9-10**: Maximum effort, no conversation possible
                """)
            
            if 'warmup_bike' in details:
                bike = details['warmup_bike']
                st.info(f"**{bike['name']}** - {bike['duration']} ({bike['intensity']})")
                
                # Add RPE tracking for bike
                bike_rpe = st.slider("Bike RPE (1-10)", 1, 10, 
                                   st.session_state.workout_data.get('bike_rpe', 5), 
                                   key="bike_rpe",
                                   help="Rate your perceived exertion during the bike warm-up")
                
                bike_completed = st.checkbox("Bike warm-up completed", 
                                           value=st.session_state.workout_data.get('bike_completed', False))
                bike_notes = st.text_area("Bike notes (optional):", height=80,
                                        value=st.session_state.workout_data.get('bike_notes', ''))
            else:
                st.info("No bike warm-up for this workout")
                bike_completed = True
                bike_notes = ""
                bike_rpe = 0
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.workout_section = 'pre_workout'
                    st.rerun()
            with col2:
                if st.button("Next: Mobility →"):
                    st.session_state.workout_data.update({
                        'bike_completed': bike_completed,
                        'bike_notes': bike_notes,
                        'bike_rpe': bike_rpe
                    })
                    st.session_state.workout_section = 'mobility'
                    st.rerun()
        
        # Mobility section
        elif st.session_state.workout_section == 'mobility':
            st.markdown("### 🤸 Mobility Warm-up")
            
            # Mobility RPE Framework
            with st.expander("🤸 Mobility RPE Framework"):
                st.markdown("""
                **Mobility-Specific RPE Scale:**
                - **1-3**: Very light stretch, minimal sensation
                - **4-5**: Moderate stretch, comfortable tension
                - **6-7**: Good stretch, noticeable but not painful
                - **8-9**: Deep stretch, approaching discomfort
                - **10**: Maximum stretch, at edge of comfort
                """)
            
            warmup_completed = st.session_state.workout_data.get('warmup_completed', {})
            
            # Mobility exercise descriptions
            mobility_descriptions = {
                "World's Greatest Stretch": "Step into lunge, place inside hand on ground, reach opposite arm to sky. Great for hips and thoracic spine.",
                "Arm Circles + Shoulder Rolls": "Large arm circles forward and backward, followed by shoulder rolls to warm up shoulder joints.",
                "Bodyweight Squats": "Deep squats focusing on full range of motion to activate glutes and warm up hip joints.",
                "Cat-Cow": "On hands and knees, arch and round spine to mobilize vertebrae.",
                "Glute Bridge March": "Hold bridge position, alternate lifting each leg to activate glutes.",
                "Hamstring Scoops": "Standing hamstring stretch with scooping motion to lengthen posterior chain.",
                "Deep Squat + Reach": "Hold deep squat position and reach arms overhead to open hips and thoracic spine.",
                "T-Spine Openers": "Lying on side, open top arm to ceiling to improve thoracic rotation.",
                "Hip CARs": "Controlled articular rotations - slow, controlled hip circles in all ranges of motion."
            }
            
            for move in details.get("mobility", []):
                st.markdown(f"**{move['name']}** - {move.get('reps', move.get('duration', ''))}")
                description = mobility_descriptions.get(move['name'], "Perform this mobility exercise with control and focus on quality of movement.")
                st.caption(description)
                
                warmup_completed[move['name']] = st.checkbox(
                    f"Completed {move['name']}",
                    value=warmup_completed.get(move['name'], False),
                    key=f"warmup_{move['name']}"
                )
                st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.workout_section = 'warmup_bike'
                    st.rerun()
            with col2:
                if st.button("Next: Supersets →"):
                    st.session_state.workout_data['warmup_completed'] = warmup_completed
                    st.session_state.workout_section = 'supersets'
                    st.rerun()
        
        # Supersets section
        elif st.session_state.workout_section == 'supersets':
            st.markdown("### 🏋️ Supersets")
            superset_logs = st.session_state.workout_data.get('superset_logs', [])
            
            for superset_idx, superset in enumerate(details.get("supersets", [])):
                st.subheader(f"{superset['title']} - {superset.get('sets', 4)} sets")
                
                for ex_idx, ex in enumerate(superset["exercises"]):
                    st.markdown(f"**{ex['name']}** - {ex['reps']}")
                    if ex.get("desc"):
                        st.caption(ex["desc"])
                    
                    # Show last week's performance for this exercise
                    last_week_performance = get_last_week_exercise_data(ex['name'], workout_day)
                    if last_week_performance:
                        st.caption(f"🔄 Last week: {last_week_performance}")
                    
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
                    
                    if len(superset_logs) <= superset_idx * len(superset["exercises"]) + ex_idx:
                        superset_logs.append({
                            "exercise": ex["name"],
                            "planned_reps": ex["reps"],
                            "sets": exercise_sets
                        })
                    else:
                        superset_logs[superset_idx * len(superset["exercises"]) + ex_idx] = {
                            "exercise": ex["name"],
                            "planned_reps": ex["reps"],
                            "sets": exercise_sets
                        }
                    
                    st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.workout_section = 'mobility'
                    st.rerun()
            with col2:
                if st.button("Next: Core Finisher →"):
                    st.session_state.workout_data['superset_logs'] = superset_logs
                    st.session_state.workout_section = 'core_finisher'
                    st.rerun()
        
        # Core finisher section
        elif st.session_state.workout_section == 'core_finisher':
            st.markdown("### 💪 Core Finisher")
            if 'core_finisher' in details:
                core_completed = st.session_state.workout_data.get('core_completed', {})
                
                for ex in details['core_finisher']:
                    core_completed[ex['name']] = st.checkbox(
                        f"{ex['name']} - {ex['reps']}",
                        value=core_completed.get(ex['name'], False),
                        key=f"core_{ex['name']}"
                    )
                
                st.session_state.workout_data['core_completed'] = core_completed
            else:
                st.info("No core finisher for this workout")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.workout_section = 'supersets'
                    st.rerun()
            with col2:
                if st.button("Next: Post-Workout →"):
                    st.session_state.workout_section = 'post_workout'
                    st.rerun()
        
        # Post-workout section
        elif st.session_state.workout_section == 'post_workout':
            st.markdown("### 🔄 Post-Workout Assessment")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("**Energy Framework**\n1 = depleted\n5 = functional but tired\n10 = fully energized")
                post_energy = st.slider("Post-Energy (1-10)", 1, 10, 
                                       st.session_state.workout_data.get('post_energy', 5), key="post_energy")
            with col2:
                st.info("**Mood Framework**\n1 = anxious/irritable\n5 = neutral\n10 = positive/uplifted")
                post_mood = st.slider("Post-Mood (1-10)", 1, 10, 
                                     st.session_state.workout_data.get('post_mood', 5), key="post_mood")
            with col3:
                st.info("**Recovery Framework**\n1 = sore/exhausted\n5 = okay\n10 = fully recovered")
                post_recovery = st.slider("Post-Recovery (1-10)", 1, 10, 
                                         st.session_state.workout_data.get('post_recovery', 5), key="post_recovery")
            
            # Cool-down
            st.markdown("### 🧘 Cool-down")
            cooldown_notes = st.text_area("Cool-down notes:", height=80,
                                         value=st.session_state.workout_data.get('cooldown_notes', ''))
            
            # Notes and auto-tagging
            st.markdown("### 📝 Notes & Tags")
            workout_notes = st.text_area("Workout notes:", height=100,
                                        value=st.session_state.workout_data.get('workout_notes', ''))
            
            # Auto-generated tags
            superset_logs = st.session_state.workout_data.get('superset_logs', [])
            completed_sets = sum(1 for log in superset_logs for s in log["sets"] if s["completed"])
            total_sets = sum(len(log["sets"]) for log in superset_logs)
            
            auto_tags = []
            if completed_sets > total_sets * 0.8:
                auto_tags.append("#goal_hit")
            if total_sets > 0:
                avg_rpe = sum(s["rpe"] for log in superset_logs for s in log["sets"]) / max(total_sets, 1)
                if avg_rpe >= 8:
                    auto_tags.append("#high_intensity")
            auto_tags.append("#consistency")
            
            selected_tags = st.multiselect("Tags:", auto_tags, 
                                         default=st.session_state.workout_data.get('selected_tags', auto_tags))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.workout_section = 'core_finisher'
                    st.rerun()
            with col2:
                if st.button("💾 Save Workout Log"):
                    # Compile final workout entry
                    workout_entry = {
                        "day": workout_day,
                        "title": details['title'],
                        "timestamp": datetime.now().isoformat(),
                        "pre_scores": {
                            "energy": st.session_state.workout_data.get('pre_energy', 5), 
                            "mood": st.session_state.workout_data.get('pre_mood', 5), 
                            "recovery": st.session_state.workout_data.get('pre_recovery', 5)
                        },
                        "bike_completed": st.session_state.workout_data.get('bike_completed', False),
                        "bike_notes": st.session_state.workout_data.get('bike_notes', ''),
                        "warmup_completed": st.session_state.workout_data.get('warmup_completed', {}),
                        "supersets": superset_logs,
                        "core_completed": st.session_state.workout_data.get('core_completed', {}),
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
                    
                    # Reset for next workout
                    st.session_state.workout_page = 'landing'
                    st.session_state.workout_section = 'pre_workout'
                    st.session_state.workout_data = {}
    
    elif st.session_state.workout_page == 'custom':
        st.subheader("Custom Workout (Coming Soon)")
        st.info("Custom workout creation will be implemented here")
        
        if st.button("← Back to Workout Selection"):
            st.session_state.workout_page = 'landing'
            st.rerun()

def landing_page():
    """Landing page showing all modules"""
    st.title("🌊 LatticeFlow")
    st.markdown("### Welcome to your integrated journaling and wellness system")
    
    # Module cards in a grid layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Journaling modules
        st.markdown("#### 📝 Journaling")
        
        with st.container():
            st.markdown("**🌅 AM Journal**")
            st.markdown("Start your day with intention and clarity")
            if st.button("Start Morning Routine", key="landing_am"):
                st.session_state.current_section = "AM Journal"
                st.session_state.show_landing = False
                st.session_state.journal_page = 'start'
                st.rerun()
        
        st.markdown("")
        
        with st.container():
            st.markdown("**🌙 PM Journal**")
            st.markdown("Reflect on your day and process experiences")
            if st.button("Start Evening Routine", key="landing_pm"):
                st.session_state.current_section = "PM Journal"
                st.session_state.show_landing = False
                st.session_state.journal_page = 'start'
                st.rerun()
        
        st.markdown("")
        
        # Mental Tools
        st.markdown("#### 🧠 Mental Tools")
        
        with st.container():
            st.markdown("**🧠 Memory Board**")
            st.markdown("Capture ideas and important reminders")
            if st.button("Open Memory Board", key="landing_memory"):
                st.session_state.current_section = "Memory Board"
                st.session_state.show_landing = False
                st.rerun()
        
        st.markdown("")
        
        with st.container():
            st.markdown("**🎯 ADHD Toolkit**")
            st.markdown("Focus tools and coping strategies")
            if st.button("Open ADHD Toolkit", key="landing_adhd"):
                st.session_state.current_section = "ADHD Toolkit"
                st.session_state.show_landing = False
                st.rerun()
    
    with col2:
        # Physical modules
        st.markdown("#### 💪 Physical")
        
        with st.container():
            st.markdown("**🏋️ Workout Tracker**")
            st.markdown("Log workouts with RPE and energy tracking")
            if st.button("Track Workout", key="landing_workout"):
                st.session_state.current_section = "Workout Tracker"
                st.session_state.show_landing = False
                st.rerun()
        
        st.markdown("")
        
        with st.container():
            st.markdown("**🍎 Macro Tracking**")
            st.markdown("Nutrition tracking and food reference")
            if st.button("View Macros", key="landing_macro"):
                st.session_state.current_section = "Macro Tracking"
                st.session_state.show_landing = False
                st.rerun()
        
        st.markdown("")
        
        # System modules
        st.markdown("#### ⚙️ System")
        
        with st.container():
            st.markdown("**🔍 Diagnostics**")
            st.markdown("System health and validation")
            if st.button("Run Diagnostics", key="landing_diagnostics"):
                st.session_state.current_section = "Diagnostics"
                st.session_state.show_landing = False
                st.rerun()
        
        st.markdown("")
        
        with st.container():
            st.markdown("**⚙️ Settings**")
            st.markdown("Configure preferences and API keys")
            if st.button("Open Settings", key="landing_settings"):
                st.session_state.current_section = "Settings"
                st.session_state.show_landing = False
                st.rerun()
    
    # Quick stats or recent activity could go here
    st.markdown("---")
    st.markdown("*Choose a module above to get started*")

def get_last_week_exercise_data(exercise_name, workout_day):
    """Get last week's performance for a specific exercise"""
    try:
        with open("kinetica-forge/workout_history.json", "r") as f:
            history = json.load(f)
        
        # Find last week's workout for this day
        for date_str, entries in history.items():
            if isinstance(entries, list):
                for entry in entries:
                    if entry.get('day') == workout_day:
                        supersets = entry.get('supersets', [])
                        for log in supersets:
                            if log.get('exercise') == exercise_name:
                                sets_data = log.get('sets', [])
                                if sets_data:
                                    # Get average RPE and typical reps
                                    avg_rpe = sum(s.get('rpe', 7) for s in sets_data) / len(sets_data)
                                    typical_reps = sets_data[0].get('reps', 'N/A')
                                    return f"{typical_reps} reps @ RPE {avg_rpe:.1f}"
        return None
    except FileNotFoundError:
        return None

def show_weekly_progression():
    """Show last week's workout performance to guide this week's training"""
    try:
        with open("kinetica-forge/workout_history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        return
    
    # Get last week's data
    from datetime import datetime, timedelta
    
    last_week_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    last_week_entries = {}
    
    # Collect last week's workouts
    for date_str, entries in history.items():
        if isinstance(entries, list):
            for entry in entries:
                if entry.get('day'):
                    last_week_entries[entry['day']] = entry
    
    if last_week_entries:
        with st.expander("📊 Last Week's Performance Review", expanded=True):
            st.info("Use last week's data to guide this week's progression:")
            
            for day, entry in last_week_entries.items():
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**{day.title()}**: {entry.get('title', 'N/A')}")
                    
                with col2:
                    # Show average RPE
                    supersets = entry.get('supersets', [])
                    if supersets:
                        total_rpe = sum(s['rpe'] for log in supersets for s in log.get('sets', []) if 'rpe' in s)
                        total_sets = sum(len(log.get('sets', [])) for log in supersets)
                        avg_rpe = round(total_rpe / max(total_sets, 1), 1) if total_sets > 0 else 0
                        st.metric("Avg RPE", f"{avg_rpe}/10")
                    
                with col3:
                    # Show completion rate
                    if supersets:
                        completed = sum(s.get('completed', False) for log in supersets for s in log.get('sets', []))
                        total = sum(len(log.get('sets', [])) for log in supersets)
                        completion_rate = round((completed / max(total, 1)) * 100) if total > 0 else 0
                        st.metric("Completion", f"{completion_rate}%")
                
                # Progression suggestions
                if supersets:
                    with st.expander(f"Progression Notes for {day.title()}"):
                        for log in supersets:
                            exercise_name = log.get('exercise', 'Unknown')
                            sets_data = log.get('sets', [])
                            if sets_data:
                                avg_rpe = sum(s.get('rpe', 7) for s in sets_data) / len(sets_data)
                                if avg_rpe < 7:
                                    st.success(f"✅ {exercise_name}: Consider increasing weight/reps (RPE was {avg_rpe:.1f})")
                                elif avg_rpe > 8.5:
                                    st.warning(f"⚠️ {exercise_name}: Consider reducing intensity (RPE was {avg_rpe:.1f})")
                                else:
                                    st.info(f"➡️ {exercise_name}: Maintain current progression (RPE was {avg_rpe:.1f})")
            
            st.markdown("**💡 Progression Tips:**")
            st.markdown("- RPE 6-7: Increase weight or reps")
            st.markdown("- RPE 7-8: Perfect progression zone") 
            st.markdown("- RPE 8+: Maintain or slightly reduce")

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

def macro_tracking():
    """Macro tracking with mobile-optimized OCR support"""
    st.header("🍎 Macro Tracking")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Macro Cheat Sheet", "📱 Label Scanner", "🛒 Grocery List", "📖 Meal Planning"])
    
    with tab1:
        st.info("Quick macro reference for common foods.")
        
        # Common foods data with full nutritional information
        import pandas as pd
        
        common_foods_data = [
            {"Name": "Chicken breast", "Category": "Protein", "Serving Size": "100g", "Calories": 165, "Protein (g)": 23, "Carbs (g)": 0, "Fat (g)": 3.6},
            {"Name": "Eggs", "Category": "Protein", "Serving Size": "1 large", "Calories": 70, "Protein (g)": 6, "Carbs (g)": 0.6, "Fat (g)": 5},
            {"Name": "Greek yogurt", "Category": "Protein", "Serving Size": "100g", "Calories": 59, "Protein (g)": 10, "Carbs (g)": 3.6, "Fat (g)": 0.4},
            {"Name": "Salmon", "Category": "Protein", "Serving Size": "100g", "Calories": 208, "Protein (g)": 20, "Carbs (g)": 0, "Fat (g)": 12},
            {"Name": "Rice (cooked)", "Category": "Carbs", "Serving Size": "100g", "Calories": 130, "Protein (g)": 2.7, "Carbs (g)": 28, "Fat (g)": 0.3},
            {"Name": "Oats (dry)", "Category": "Carbs", "Serving Size": "50g", "Calories": 190, "Protein (g)": 6.8, "Carbs (g)": 32, "Fat (g)": 3.4},
            {"Name": "Sweet potato", "Category": "Carbs", "Serving Size": "100g", "Calories": 86, "Protein (g)": 1.6, "Carbs (g)": 20, "Fat (g)": 0.1},
            {"Name": "Banana", "Category": "Carbs", "Serving Size": "1 medium", "Calories": 105, "Protein (g)": 1.3, "Carbs (g)": 27, "Fat (g)": 0.4},
            {"Name": "Olive oil", "Category": "Fats", "Serving Size": "1 tbsp", "Calories": 120, "Protein (g)": 0, "Carbs (g)": 0, "Fat (g)": 14},
            {"Name": "Avocado", "Category": "Fats", "Serving Size": "100g", "Calories": 160, "Protein (g)": 2, "Carbs (g)": 9, "Fat (g)": 15},
            {"Name": "Almonds", "Category": "Fats", "Serving Size": "28g", "Calories": 164, "Protein (g)": 6, "Carbs (g)": 6, "Fat (g)": 14},
            {"Name": "Peanut butter", "Category": "Fats", "Serving Size": "2 tbsp", "Calories": 190, "Protein (g)": 8, "Carbs (g)": 8, "Fat (g)": 16}
        ]
        
        # Create DataFrame and display as table
        df = pd.DataFrame(common_foods_data)
        
        # Add category filter
        categories = ["All"] + list(df["Category"].unique())
        selected_category = st.selectbox("Filter by category:", categories)
        
        if selected_category != "All":
            filtered_df = df[df["Category"] == selected_category]
        else:
            filtered_df = df
        
        # Display table
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Add search functionality
        search_term = st.text_input("Search foods:", placeholder="e.g., chicken, oats...")
        if search_term:
            search_df = df[df["Name"].str.contains(search_term, case=False)]
            if not search_df.empty:
                st.markdown("### Search Results")
                st.dataframe(search_df, use_container_width=True, hide_index=True)
            else:
                st.info("No foods found matching your search.")
    
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
                    st.caption(f"🏷️ {card['type']}")
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
    
    # Show landing page or selected section
    if st.session_state.show_landing:
        landing_page()
    elif section == "AM Journal":
        am_journal()
    elif section == "PM Journal":
        pm_journal()
    elif section == "Workout Tracker":
        workout_tracker()
    elif section == "Macro Tracking":
        macro_tracking()
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
