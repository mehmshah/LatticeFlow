
import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

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

# --- Improved authentication ---
def authenticate():
    """Secure authentication with session state"""
    if st.session_state.authenticated:
        return True
    
    st.sidebar.title("🌊 LatticeFlow")
    st.sidebar.markdown("---")
    
    # Get password from secrets or use dummy password
    correct_password = get_secret("APP_PASSWORD") or "lattice123"
    
    password = st.sidebar.text_input("Password", type="password", key="auth_password")
    
    if st.sidebar.button("Login"):
        if password == correct_password:
            st.session_state.authenticated = True
            st.sidebar.success("✅ Authenticated!")
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid password")
    
    if not st.session_state.authenticated:
        st.sidebar.warning("🔐 Please login to access the app")
        if correct_password == "lattice123":
            st.sidebar.info("💡 Using dummy password: lattice123")
        st.stop()

# --- Enhanced navigation ---
def sidebar_navigation():
    """Enhanced sidebar navigation with icons and organization"""
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
                st.rerun()
    
    # Add logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()
    
    return st.session_state.current_section

# --- Enhanced placeholder functions ---
def am_journal():
    """AM Journal with conversational flow"""
    st.header("🌅 AM Journal")
    
    # Create tabs for different aspects
    tab1, tab2, tab3 = st.tabs(["💬 Reflection", "📊 Metrics", "📋 Summary"])
    
    with tab1:
        st.info("Start your day with reflection and intention setting.")
        
        # Conversational flow
        if 'am_step' not in st.session_state:
            st.session_state.am_step = 0
        
        steps = [
            "How did you sleep? How's your energy?",
            "What's your main intention for today?",
            "Any worries or concerns to address?",
            "What are you grateful for this morning?"
        ]
        
        if st.session_state.am_step < len(steps):
            st.write(f"**Step {st.session_state.am_step + 1}:** {steps[st.session_state.am_step]}")
            response = st.text_area("Your response:", key=f"am_response_{st.session_state.am_step}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Next") and response.strip():
                    st.session_state.am_step += 1
                    st.rerun()
            with col2:
                if st.button("Reset Flow"):
                    st.session_state.am_step = 0
                    st.rerun()
        else:
            st.success("✅ Morning reflection complete!")
            if st.button("Start New Reflection"):
                st.session_state.am_step = 0
                st.rerun()
    
    with tab2:
        st.info("Metric scoring and tracking coming soon...")
        # TODO: Implement metric scoring system
    
    with tab3:
        st.info("GPT-powered summaries coming soon...")
        # TODO: Implement GPT summarization

def pm_journal():
    """PM Journal with day review"""
    st.header("🌙 PM Journal")
    
    tab1, tab2, tab3 = st.tabs(["💭 Reflection", "🏷️ Tags", "📈 Trends"])
    
    with tab1:
        st.info("Reflect on your day and prepare for tomorrow.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Day Review")
            day_reflection = st.text_area("How was your day overall?", height=100)
            relationships = st.text_area("How were your relationships today?", height=100)
        
        with col2:
            st.subheader("Forward Looking")
            tomorrow_prep = st.text_area("What do you want to focus on tomorrow?", height=100)
            gratitude = st.text_area("What are you grateful for today?", height=100)
        
        if st.button("Generate Summary"):
            st.info("GPT analysis coming soon...")
    
    with tab2:
        st.info("Emotion tagging and analysis coming soon...")
    
    with tab3:
        st.info("Trend analysis and insights coming soon...")

def workout_tracker():
    """Enhanced workout tracking"""
    st.header("💪 Workout Tracker")
    
    tab1, tab2, tab3 = st.tabs(["🏋️ Today's Workout", "📊 RPE & Energy", "📈 History"])
    
    with tab1:
        st.info("Log your workout with detailed tracking.")
        
        # Pre-workout scoring
        st.subheader("Pre-Workout Assessment")
        col1, col2, col3 = st.columns(3)
        with col1:
            pre_energy = st.slider("Energy Level", 1, 10, 5, key="pre_energy")
        with col2:
            pre_mood = st.slider("Mood", 1, 10, 5, key="pre_mood")
        with col3:
            pre_recovery = st.slider("Recovery", 1, 10, 5, key="pre_recovery")
        
        # Workout logging
        st.subheader("Workout Log")
        workout_type = st.selectbox("Workout Type", ["Push", "Pull", "Legs", "Cardio", "Other"])
        
        # Dynamic exercise logging
        if 'exercises' not in st.session_state:
            st.session_state.exercises = []
        
        with st.expander("Add Exercise"):
            exercise_name = st.text_input("Exercise Name")
            sets = st.number_input("Sets", min_value=1, max_value=20, value=3)
            reps = st.text_input("Reps (e.g., 10, 8-12, or 30s)")
            if st.button("Add Exercise"):
                st.session_state.exercises.append({
                    'name': exercise_name,
                    'sets': sets,
                    'reps': reps,
                    'completed': False
                })
                st.rerun()
        
        # Display exercises
        for i, exercise in enumerate(st.session_state.exercises):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{exercise['name']}** - {exercise['sets']} sets of {exercise['reps']}")
            with col2:
                completed = st.checkbox("Done", key=f"exercise_{i}")
                st.session_state.exercises[i]['completed'] = completed
            with col3:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.exercises.pop(i)
                    st.rerun()
    
    with tab2:
        st.info("RPE tracking and energy analysis...")
        rpe = st.slider("Overall RPE (Rate of Perceived Exertion)", 1, 10, 5)
        st.write(f"RPE: {rpe}/10")
    
    with tab3:
        st.info("Workout history and progress tracking coming soon...")

def macro_cheat_sheet():
    """Macro tracking with OCR support"""
    st.header("🍎 Macro Cheat Sheet")
    
    tab1, tab2, tab3 = st.tabs(["📊 Quick Reference", "📱 Label Scanner", "🛒 Grocery List"])
    
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
        st.info("📱 OCR label scanning coming soon...")
        uploaded_file = st.file_uploader("Upload food label image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded label")
            st.info("OCR processing will be implemented here")
    
    with tab3:
        st.info("🛒 Grocery tracking and meal planning...")

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
    
    # Header
    st.title("🌊 LatticeFlow")
    st.markdown("*Modular Journaling & Workout System*")
    st.markdown("---")
    
    # Route to appropriate section
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
