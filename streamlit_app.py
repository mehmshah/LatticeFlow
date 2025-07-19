
import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import sys

# --- LLM Service Import ---
import llm_service  # Centralized LLM API calls

# --- GLOBAL MOBILE CSS ---
st.markdown('''
    <style>
    html, body, [class*="css"]  {
        font-size: 18px !important;
    }
    @media (max-width: 750px) {
        .block-container {
            padding: 0.5rem 0.2rem 2rem 0.2rem !important;
        }
        .stButton > button, .stDownloadButton > button {
            width: 100% !important;
            min-height: 48px !important;
            font-size: 1.12em !important;
        }
        .stTextInput > div > input, .stTextArea > div > textarea {
            font-size: 1.08em !important;
        }
        .stSlider > div {
            font-size: 1.08em !important;
        }
    }
    </style>
''', unsafe_allow_html=True)

st.markdown('''
    <style>
    html, body, [class*="css"]  {
        font-size: 18px !important;
    }
    @media (max-width: 750px) {
        .block-container {
            padding: 0.5rem 0.2rem 2rem 0.2rem !important;
        }
        .stButton > button, .stDownloadButton > button {
            width: 100% !important;
            min-height: 48px !important;
            font-size: 1.15rem !important;
            margin-bottom: 0.5rem !important;
        }
        .stTextArea textarea, .stTextInput input {
            font-size: 1.1rem !important;
            min-height: 48px !important;
        }
        .stExpanderHeader {
            font-size: 1.25rem !important;
        }
        .stMarkdown, .stCaption, .stSubheader {
            font-size: 1.1rem !important;
        }
        .stMultiSelect > div {
            font-size: 1.1rem !important;
        }
        .stExpander {
            margin-bottom: 1.5rem !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            flex-direction: column !important;
        }
        .stTabs [data-baseweb="tab"] {
            width: 100% !important;
            min-height: 48px !important;
            font-size: 1.1rem !important;
        }
        .stRadio [role="radiogroup"] {
            flex-direction: column !important;
        }
        .stRadio [data-baseweb="radio"] {
            margin-bottom: 0.5rem !important;
        }
        .stDataFrameContainer {
            font-size: 1rem !important;
        }
    }
    </style>
''', unsafe_allow_html=True)

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
            return load_json('user_preferences.json', default={
    'theme': 'light',
    'api_keys': {},
    'default_metrics': {}
})
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
        atomic_save_json('user_preferences.json', preferences)
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
import onboarding
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
                "⚙️ System": ["Diagnostics", "Journal Setup", "Settings"]
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

def landing_page():
    """
    Improved landing page for LatticeFlow onboarding UX.
    Explains app purpose, onboarding importance, and provides call-to-action.
    """
    st.title("🌊 Welcome to LatticeFlow")
    st.markdown("""
    #### Your Modular Journaling, Wellness, and Diagnostics Companion
    LatticeFlow helps you build daily reflection, track routines, and gain insights with AI-powered analysis.
    
    **To get started, you must complete a brief onboarding.**
    This will configure your journaling experience and unlock all modules.
    """)
    st.info("Onboarding is required before you can use the journaling and diagnostics features.")
    if st.button("🚀 Start Onboarding", key="landing_onboarding_cta", use_container_width=True):
        st.session_state.show_landing = False
        st.experimental_rerun()
    st.markdown("---")
    st.markdown("*LatticeFlow © 2025 | Built with Streamlit*")

def diagnostics():
    """Diagnostics and unified journaling review page with macro/workout logs and LLM-powered diagnostics preview. Enhanced for mobile."""
    # --- MOBILE CSS ---
    st.markdown('''
        <style>
        html, body, [class*="css"]  {
            font-size: 18px !important;
        }
        @media (max-width: 750px) {
            .block-container {
                padding: 0.5rem 0.2rem 2rem 0.2rem !important;
            }
            .stButton > button, .stDownloadButton > button {
                width: 100% !important;
                min-height: 48px !important;
                font-size: 1.15rem !important;
                margin-bottom: 0.5rem !important;
            }
            .stTextArea textarea, .stTextInput input {
                font-size: 1.1rem !important;
                min-height: 48px !important;
            }
            .stExpanderHeader {
                font-size: 1.25rem !important;
            }
            .stMarkdown, .stCaption, .stSubheader {
                font-size: 1.1rem !important;
            }
            .stMultiSelect > div {
                font-size: 1.1rem !important;
            }
            .stExpander {
                margin-bottom: 1.5rem !important;
            }
        }
        </style>
    ''', unsafe_allow_html=True)
    st.header("🩺 Journaling & Diagnostics")
    import glob
    # Load tag lists
    try:
        with open('aether-core/instruction_engine.json', 'r') as f:
            instructions = json.load(f)
        tag_lists = instructions['tagging_logic']
        all_tags = tag_lists['emotion_tags'] + tag_lists['relationship_tags'] + tag_lists['theme_tags']
    except Exception:
        all_tags = []
    # Collect entries
    entries = []
    # AM logs
    for fname in sorted(glob.glob('vesper-archive/am_log_*.json'), reverse=True):
        with open(fname, 'r') as f:
            entry = json.load(f)
            entry['type'] = 'AM'
            entries.append(entry)
    # PM logs
    for fname in sorted(glob.glob('vesper-archive/pm_log_*.json'), reverse=True):
        with open(fname, 'r') as f:
            entry = json.load(f)
            entry['type'] = 'PM'
            entries.append(entry)
    # Macro logs (archive)
    for fname in sorted(glob.glob('vesper-archive/macro_log_*.json'), reverse=True):
        with open(fname, 'r') as f:
            entry = json.load(f)
            entry['type'] = 'Macro'
            entries.append(entry)
    # Workout logs (archive)
    for fname in sorted(glob.glob('vesper-archive/workout_log_*.json'), reverse=True):
        with open(fname, 'r') as f:
            entry = json.load(f)
            entry['type'] = 'Workout'
            entries.append(entry)
    # Macro logs (session)
    if 'macro_logs' in st.session_state:
        for m in st.session_state['macro_logs']:
            e = dict(m)
            e['type'] = 'Macro'
            entries.append(e)
    # Workout logs (session)
    if 'workout_logs' in st.session_state:
        for w in st.session_state['workout_logs']:
            e = dict(w)
            e['type'] = 'Workout'
            entries.append(e)
    # Tag filter (stacked for mobile)
    st.markdown('<div style="margin-bottom:0.5rem"></div>', unsafe_allow_html=True)
    selected_tags = st.multiselect("Filter by tag", all_tags)
    st.markdown('<div style="margin-bottom:0.5rem"></div>', unsafe_allow_html=True)
    filtered = [e for e in entries if not selected_tags or any(t in (e.get('tags', [])) for t in selected_tags)]
    # Export all filtered entries (stacked)
    st.markdown('---')
    st.download_button(
        label="Export All (JSON)",
        data=json.dumps(filtered, indent=2),
        file_name=f"latticeflow_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        key="export_all_json_btn"
    )
    st.download_button(
        label="Export All (Markdown)",
        data='\n'.join([
            f"### {e['type']} — {e.get('timestamp','')[:10]}\n**Reflection:** {e.get('reflection','')}\n**Tags:** {', '.join(e.get('tags', []))}\n**Relationships:** {e.get('relationships','')}\n**Scores:** {e.get('scores','')}\n---" for e in filtered]),
        file_name=f"latticeflow_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown",
        key="export_all_md_btn"
    )
    st.markdown('---')
    # Mobile-friendly: vertical stack for entries
    for entry in filtered:
        with st.expander(f"{entry['type']} — {entry.get('timestamp','')[:10]}"):
            st.markdown(f"<div style='font-size:1.12rem;line-height:1.5;'><b>Reflection:</b> {entry.get('reflection','')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:1.12rem;'><b>Tags:</b> {', '.join(entry.get('tags', []))}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:1.12rem;'><b>Relationships:</b> {entry.get('relationships','')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:1.12rem;'><b>Scores:</b> {entry.get('scores','')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.98rem;color:#888;'><b>Other:</b> {json.dumps(entry, indent=2)}</div>", unsafe_allow_html=True)
            # Per-entry export (vertical)
            st.download_button(
                label="Export as JSON",
                data=json.dumps(entry, indent=2),
                file_name=f"{entry['type'].lower()}_entry_{entry.get('timestamp','').replace(':','').replace('-','')}.json",
            )
            if entry['type'] == 'Macro':
                if st.button(f"Analyze Macros", key=f"diag_macro_{entry.get('timestamp','')}"):
                    with st.spinner("Analyzing macros with GPT..."):
                        macro_query = entry.get('reflection','') or entry.get('macros','')
                        macro_result = llm_service.analyze_macros(macro_query)
                        st.info(macro_result)
            elif entry['type'] == 'Workout':
                if st.button(f"Analyze Workout", key=f"diag_workout_{entry.get('timestamp','')}"):
                    with st.spinner("Analyzing workout with GPT..."):
                        workout_query = entry.get('reflection','') or entry.get('workout_log','')
                        feedback = llm_service.get_workout_feedback(workout_query)
                        st.info(feedback)

def pm_journal(user_config=None):
    """PM Journal with dynamic, modular, session-state-driven navigation."""
    import streamlit as st
    from datetime import datetime
    import os
    import json

    # --- Initialize PM session state ---
    if 'pm_data' not in st.session_state:
        st.session_state.pm_data = {}
    if 'journal_page' not in st.session_state or not st.session_state.journal_page.startswith('pm_'):
        st.session_state.journal_page = 'pm_pause'

    # --- Define enabled steps based on config ---
    toggles = (user_config or {}).get('toggles', {})
    steps = []
    if toggles.get('mantra', True):
        steps.append('pm_pause')
    steps.append('pm_reflection')
    if user_config and user_config.get('metrics'):
        steps.append('pm_metrics')
    if toggles.get('calendar', False) or toggles.get('weather', False):
        steps.append('pm_calendar_weather')
    if toggles.get('adhd', False):
        steps.append('pm_memory_board')
    steps.append('pm_trends')
    steps.append('pm_complete')

    # --- Navigation helpers ---
    def next_step():
        idx = steps.index(st.session_state.journal_page)
        if idx < len(steps) - 1:
            st.session_state.journal_page = steps[idx+1]
            st.rerun()
    def prev_step():
        idx = steps.index(st.session_state.journal_page)
        if idx > 0:
            st.session_state.journal_page = steps[idx-1]
            st.rerun()

    # --- Modular step rendering ---
    page = st.session_state.journal_page
    if page == 'pm_pause':
        st.header("🌙 PM Journal — Pause/Mantra")
        st.info("[Pause/Mantra step placeholder]")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Next →", on_click=next_step, key="pm_next_pause")
    elif page == 'pm_reflection':
        st.header("🌙 PM Journal — Free Reflection")
        st.caption("Write about your day, thoughts, or anything on your mind. Click 'Analyze & Tag' to get AI-powered emotions and themes.")

        # Prefill reflection and tags if present
        reflection = st.text_area(
            "Evening Reflection",
            value=st.session_state.pm_data.get('reflection', ''),
            height=200,
            key="pm_reflection_text"
        )
        tags = st.session_state.pm_data.get('tags', [])
        emotional_tags = st.session_state.pm_data.get('emotional_tags', [])
        tag_error = None
        analyzed = False

        if st.button("Analyze & Tag", key="pm_analyze_tag"):
            if reflection.strip():
                try:
                    import llm_service
                    result = llm_service.tag_journal_entry(reflection)
                    # Expecting result as {"emotions": [...], "themes": [...]}
                    if isinstance(result, str):
                        import json
                        result = json.loads(result)
                    tags = result.get('themes', [])
                    emotional_tags = result.get('emotions', [])
                    st.session_state.pm_data['tags'] = tags
                    st.session_state.pm_data['emotional_tags'] = emotional_tags
                    analyzed = True
                except Exception as e:
                    tag_error = f"Tagging failed: {e}"
            else:
                tag_error = "Please enter a reflection before analyzing."

        # Show tags/emotions if present
        if tags or emotional_tags:
            st.markdown(f"<b>Themes:</b> {', '.join(tags) if tags else '—'}", unsafe_allow_html=True)
            st.markdown(f"<b>Emotions:</b> {', '.join(emotional_tags) if emotional_tags else '—'}", unsafe_allow_html=True)
        if tag_error:
            st.error(tag_error)
        elif analyzed:
            st.success("Tags and emotions updated!")

        # Save reflection in pm_data
        st.session_state.pm_data['reflection'] = reflection

        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="pm_back_reflection")
        with col2:
            st.button("Next →", on_click=next_step, key="pm_next_reflection")

    elif page == 'pm_metrics':
        st.header("🌙 PM Journal — Metrics")
        st.caption("Score each metric from 1–10. You can use AI to auto-score based on your reflection.")
        metrics = (user_config or {}).get('metrics', [])
        pm_metrics = st.session_state.pm_data.get('metrics', {})
        metric_scores = {}
        metric_error = None
        auto_scored = False

        # Show sliders for each metric
        for metric in metrics:
            metric_scores[metric] = st.slider(
                metric,
                min_value=1, max_value=10,
                value=int(pm_metrics.get(metric, 5)),
                key=f"pm_metric_{metric}"
            )

        # Auto-Score with GPT
        if st.button("Auto-Score with GPT", key="pm_auto_score"):
            try:
                import llm_service
                reflection = st.session_state.pm_data.get('reflection', '')
                relationships = st.session_state.pm_data.get('relationships', '')
                result = llm_service.auto_score_pm_metrics(reflection, relationships, metrics)
                # Expecting result as {metric: score, ...}
                if isinstance(result, str):
                    import json
                    result = json.loads(result)
                for metric in metrics:
                    if metric in result:
                        metric_scores[metric] = int(result[metric]) if isinstance(result[metric], int) else 5
                st.session_state.pm_data['metrics'] = metric_scores
                auto_scored = True
            except Exception as e:
                metric_error = f"Auto-scoring failed: {e}"

        # Save scores in pm_data
        st.session_state.pm_data['metrics'] = metric_scores

        if metric_error:
            st.error(metric_error)
        elif auto_scored:
            st.success("Metrics auto-scored!")

        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="pm_back_metrics")
        with col2:
            st.button("Next →", on_click=next_step, key="pm_next_metrics")

    elif page == 'pm_calendar_weather':
        st.header("🌙 PM Journal — Calendar & Weather")
        st.info("[Calendar/Weather step placeholder]")
        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="pm_back_calendar_weather")
        with col2:
            st.button("Next →", on_click=next_step, key="pm_next_calendar_weather")
    elif page == 'pm_memory_board':
        st.header("🌙 PM Journal — Memory Board & ADHD")
        import os
        import json
        from datetime import datetime
        today = '2025-07-17'  # Use provided current date
        try:
            from beemind import load_memory_cards, load_adhd_scripts, save_memory_cards
        except Exception:
            st.error("Could not import memory board/ADHD modules.")
            return

        # Load cards if not in session state
        if 'memory_board_cards' not in st.session_state:
            try:
                st.session_state.memory_board_cards = load_memory_cards()
            except Exception:
                st.session_state.memory_board_cards = []
        if 'script_cards' not in st.session_state:
            try:
                script_raw = load_adhd_scripts()
                st.session_state.script_cards = []
            except Exception:
                st.session_state.script_cards = []
        user_cards = st.session_state.memory_board_cards
        script_cards = st.session_state.script_cards
        all_cards = user_cards + script_cards

        # --- Review Stats ---
        reviewed_today = sum(1 for c in all_cards if today in c.get('relevant_today', []))
        st.markdown(f"<div style='font-size:1.1rem;'><b>Cards reviewed today:</b> {reviewed_today} / {len(all_cards)}</div>", unsafe_allow_html=True)

        # --- Bulk Tag Editing (User Cards Only) ---
        with st.expander("Bulk Edit Tags (User Cards)"):
            all_tags = sorted({tag for c in user_cards for tag in c.get('tags', [])})
            selected_cards = st.multiselect("Select cards to edit:", [c['title'] for c in user_cards])
            new_bulk_tags = st.text_input("Add tags (comma-separated):", value="")
            if st.button("Apply Tags to Selected") and selected_cards and new_bulk_tags:
                tags_to_add = [t.strip() for t in new_bulk_tags.split(",") if t.strip()]
                for c in user_cards:
                    if c['title'] in selected_cards:
                        c['tags'] = sorted(set(c.get('tags', []) + tags_to_add))
                try:
                    save_memory_cards(user_cards)
                    st.success("Bulk tag update applied.")
                except Exception as e:
                    st.error(f"Failed to save tags: {e}")

        # --- Card Display ---
        updated = False
        for card in all_cards:
            color = "#e3f2fd" if card.get('id', '').startswith('script_') else "#f9fbe7"
            badge = f"<span style='background:#90caf9;color:#0d47a1;padding:2px 8px;border-radius:8px;margin-right:6px;font-size:0.9em;'>{card.get('category','Script')}</span>" if card.get('id', '').startswith('script_') else "<span style='background:#c5e1a5;color:#33691e;padding:2px 8px;border-radius:8px;margin-right:6px;font-size:0.9em;'>User</span>"
            with st.expander(f"{badge} {card['title']}", expanded=False):
                st.markdown(f"<div style='background:{color};padding:0.7em 1em 0.5em 1em;border-radius:10px;'>", unsafe_allow_html=True)
                st.markdown(f"<b>Description:</b> {card.get('description','—')}", unsafe_allow_html=True)
                st.markdown(f"<b>Tags:</b> {', '.join(card.get('tags', [])) or '—'}", unsafe_allow_html=True)
                st.markdown(f"<b>Content:</b> <pre style='white-space:pre-wrap;font-size:1.03em;'>{card['content']}</pre>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)


                # Tag editing for user cards
                if not card.get('id', '').startswith('script_'):
                    new_tags = st.multiselect(
                        f"Tags for {card['title']}",
                        ["focus", "routine", "emotion", "work", "AM", "PM", "success", "coping", "strategy", "custom"] + all_tags,
                        default=card.get('tags', []),
                        key=f"tags_{card['id']}"
                    )
                    if set(new_tags) != set(card.get('tags', [])):
                        card['tags'] = new_tags
                        updated = True
                # Review tracking
                last_reviewed = card.get('last_reviewed')
                st.caption(f"Last reviewed: {last_reviewed or '—'}")
                checked = today in card.get('relevant_today', [])
                key = f"relevant_today_{card['id']}"
                new_checked = st.checkbox("Relevant Today", value=checked, key=key)
                if new_checked and not checked:
                    card.setdefault('relevant_today', []).append(today)
                    card['last_reviewed'] = today
                    updated = True
                elif not new_checked and checked:
                    card['relevant_today'].remove(today)
                    updated = True
        # Save user card changes persistently
        if updated:
            try:
                save_memory_cards([c for c in all_cards if not c.get('id', '').startswith('script_')])
                st.success("Memory Board updated!")
            except Exception as e:
                st.error(f"Failed to save memory board: {e}")

        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="pm_back_memory_board")
        with col2:
            st.button("Next →", on_click=next_step, key="pm_next_memory_board")

    elif page == 'pm_trends':
        st.header("🌙 PM Journal — Trend Analysis & Insights")
        import os
        import json
        reflection = st.session_state.pm_data.get('reflection', '')
        metrics = st.session_state.pm_data.get('metrics', {})
        tags = st.session_state.pm_data.get('tags', [])
        emotional_tags = st.session_state.pm_data.get('emotional_tags', [])
        trend_error = None
        insights = st.session_state.pm_data.get('trend_insights', None)

        st.markdown("**Reflection:**")
        st.markdown(reflection or '—')
        st.markdown(f"**Metrics:** {json.dumps(metrics) if metrics else '—'}")
        st.markdown(f"**Tags:** {', '.join(tags) if tags else '—'}")
        st.markdown(f"**Emotions:** {', '.join(emotional_tags) if emotional_tags else '—'}")

        if st.button("Analyze Trends with GPT", key="pm_trends_llm"):
            try:
                import llm_service
                result = llm_service.analyze_trends([reflection])
                if isinstance(result, str):
                    insights = result
                else:
                    insights = str(result)
                st.session_state.pm_data['trend_insights'] = insights
            except Exception as e:
                trend_error = f"Trend analysis failed: {e}"

        if insights:
            st.info(insights)
        if trend_error:
            st.error(trend_error)

        # Save/Finish PM Routine
        if st.button("Finish PM Routine & Save", key="pm_finish"):
            try:
                pm_entry = {
                    "timestamp": "2025-07-17T17:56:52-04:00",
                    **st.session_state.pm_data
                }
                os.makedirs("vesper-archive", exist_ok=True)
                with open(f"vesper-archive/pm_log_20250717.json", "w") as f:
                    json.dump(pm_entry, f, indent=2)
                st.success("✅ Evening reflection saved!")
                st.balloons()
                st.session_state.journal_page = 'pm_complete'
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save PM log: {e}")

        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="pm_back_trends")
        with col2:
            st.button("Next →", on_click=next_step, key="pm_next_trends")

    elif page == 'pm_complete':
        st.header("🌙 PM Journal — Complete!")
        st.success("Your PM reflection has been saved. Well done!")
        if st.button("Start New PM Routine", key="pm_restart"):
            st.session_state.journal_page = steps[0]
            st.session_state.pm_data = {}
            st.rerun()

    # --- Review Stats ---
    today = datetime.now().strftime('%Y-%m-%d')
    reviewed_today = sum(1 for c in all_cards if today in c.get('relevant_today', []))
    st.markdown(f"<div style='font-size:1.1rem;'><b>Cards reviewed today:</b> {reviewed_today} / {len(all_cards)}</div>", unsafe_allow_html=True)

    # --- Bulk Tag Editing (User Cards Only) ---
    with st.expander("Bulk Edit Tags (User Cards)"):
        all_tags = sorted({tag for c in user_cards for tag in c.get('tags', [])})
        selected_cards = st.multiselect("Select cards to edit:", [c['title'] for c in user_cards])
        new_bulk_tags = st.text_input("Add tags (comma-separated):", value="")
        if st.button("Apply Tags to Selected") and selected_cards and new_bulk_tags:
            tags_to_add = [t.strip() for t in new_bulk_tags.split(",") if t.strip()]
            for c in user_cards:
                if c['title'] in selected_cards:
                    c['tags'] = sorted(set(c.get('tags', []) + tags_to_add))
            save_memory_cards(user_cards)
            st.success("Bulk tag update applied.")

    # --- Card Display ---
    updated = False
    for card in all_cards:
        # Color and badge logic
        color = "#e3f2fd" if card.get('id', '').startswith('script_') else "#f9fbe7"
        badge = f"<span style='background:#90caf9;color:#0d47a1;padding:2px 8px;border-radius:8px;margin-right:6px;font-size:0.9em;'>{card.get('category','Script')}</span>" if card.get('id', '').startswith('script_') else "<span style='background:#c5e1a5;color:#33691e;padding:2px 8px;border-radius:8px;margin-right:6px;font-size:0.9em;'>User</span>"
        with st.expander(f"{badge} {card['title']}", expanded=False):
            st.markdown(f"<div style='background:{color};padding:0.7em 1em 0.5em 1em;border-radius:10px;'>", unsafe_allow_html=True)
            st.markdown(f"<b>Description:</b> {card.get('description','—')}")
            st.markdown(f"<b>Tags:</b> {', '.join(card.get('tags', [])) or '—'}")
            st.markdown(f"<b>Content:</b> <pre style='white-space:pre-wrap;font-size:1.03em;'>{card['content']}</pre>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            # Tag editing for user cards
            if not card.get('id', '').startswith('script_'):
                new_tags = st.multiselect(
                    f"Tags for {card['title']}",
                    ["focus", "routine", "emotion", "work", "AM", "PM", "success", "coping", "strategy", "custom"] + all_tags,
                    default=card.get('tags', []),
                    key=f"tags_{card['id']}"
                )
                if set(new_tags) != set(card.get('tags', [])):
                    card['tags'] = new_tags
                    updated = True
            # Review tracking
            last_reviewed = card.get('last_reviewed')
            st.caption(f"Last reviewed: {last_reviewed or '—'}")
            checked = today in card.get('relevant_today', [])
            key = f"relevant_today_{card['id']}"
            new_checked = st.checkbox("Relevant Today", value=checked, key=key)
            if new_checked and not checked:
                card.setdefault('relevant_today', []).append(today)
                card['last_reviewed'] = today
                updated = True
            elif not new_checked and checked:
                card['relevant_today'].remove(today)
                updated = True
    # --- Navigation & Save ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="am_back_memory_board"):
            st.session_state.journal_page = 'mantra'
            st.rerun()
    with col2:
        if st.button("Next: Sleep & Energy →", key="am_next1_memory_board"):
            st.session_state.journal_page = 'sleep_energy'
            st.rerun()
        if updated:
            save_memory_cards([c for c in all_cards if not c.get('id', '').startswith('script_')])
            st.success("Memory Board updated!")

    if st.session_state.journal_page == 'sleep_energy':
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
        pass

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
        pass

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
                atomic_save_json(f"vesper-archive/am_log_{datetime.now().strftime('%Y%m%d')}.json", am_entry)
                
                st.success("✅ Morning reflection saved!")
                st.balloons()
                st.session_state.journal_page = 'complete'
                st.rerun()
        pass

    elif st.session_state.journal_page == 'complete':
        st.success("🎉 Morning routine complete!")
        st.info("Your morning reflection has been saved. Have a great day!")
        if st.button("Start New Morning Routine", key="am_restart"):
            st.session_state.journal_page = 'start'
            st.rerun()

    elif st.session_state.journal_page == 'metrics':
        st.subheader("Metrics")
        # ... metric scoring UI ...
        if st.button("Auto-Score with GPT", key="pm_auto_score"):
            reflection = st.session_state.pm_data.get('reflection', '')
            relationships = st.session_state.pm_data.get('relationships', '')
            metrics = list(metric_groups["metric_groups"].keys())
            with st.spinner("Scoring metrics via ChatGPT..."):
                scores = llm_service.auto_score_pm_metrics(reflection, relationships, metrics)
                st.info(scores)
        if st.button("Next: Trends", key="pm_next_trends"):
            st.session_state.journal_page = 'trends'
            st.rerun()
        pass
    elif st.session_state.journal_page == 'trends':
        st.subheader("Trend Analysis & Insights")
        # --- Trend Analysis (LLM) ---
        logs = [st.session_state.pm_data.get('reflection', '')]
        if st.button("Analyze Trends with GPT", key="pm_trends_llm"):
            with st.spinner("Analyzing trends via ChatGPT..."):
                insights = llm_service.analyze_trends(logs)
                st.info(insights)
        if st.button("Finish PM Routine", key="pm_finish"):
            st.session_state.journal_page = 'start'
            st.rerun()
        pass

def am_journal(user_config=None):
    """AM Journal with modular, session-state-driven navigation, LLM-powered diagnostics, tagging, and explicit confirmation."""
    import streamlit as st
    from datetime import datetime
    import os
    import json

    # --- Initialize AM session state ---
    if 'am_data' not in st.session_state:
        st.session_state.am_data = {}
    if 'journal_page' not in st.session_state or not st.session_state.journal_page.startswith('am_'):
        st.session_state.journal_page = 'am_pause'

    # --- Define enabled steps based on config ---
    toggles = (user_config or {}).get('toggles', {})
    steps = []
    if toggles.get('mantra', True):
        steps.append('am_pause')
    steps.append('am_reflection')
    steps.append('am_sleep_energy')
    steps.append('am_intentions')
    steps.append('am_diagnostics')
    steps.append('am_complete')

    # --- Navigation helpers ---
    def next_step():
        idx = steps.index(st.session_state.journal_page)
        if idx < len(steps) - 1:
            st.session_state.journal_page = steps[idx+1]
            st.rerun()
    def prev_step():
        idx = steps.index(st.session_state.journal_page)
        if idx > 0:
            st.session_state.journal_page = steps[idx-1]
            st.rerun()

    # --- Modular step rendering ---
    page = st.session_state.journal_page
    if page == 'am_pause':
        st.header("☀️ AM Journal — Pause/Mantra")
        st.info("[Pause/Mantra step placeholder]")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Next →", on_click=next_step, key="am_next_pause")
    elif page == 'am_reflection':
        st.header("☀️ AM Journal — Morning Reflection")
        st.caption("Write about your intentions, goals, or anything on your mind. Click 'Analyze & Tag' to get AI-powered emotions and themes.")
        reflection = st.text_area(
            "Morning Reflection",
            value=st.session_state.am_data.get('reflection', ''),
            height=200,
            key="am_reflection_text"
        )
        tags = st.session_state.am_data.get('tags', [])
        emotional_tags = st.session_state.am_data.get('emotional_tags', [])
        tag_error = None
        analyzed = False
        if st.button("Analyze & Tag", key="am_analyze_tag"):
            if reflection.strip():
                try:
                    import llm_service
                    result = llm_service.tag_journal_entry(reflection)
                    if isinstance(result, str):
                        import json
                        result = json.loads(result)
                    tags = result.get('themes', [])
                    emotional_tags = result.get('emotions', [])
                    st.session_state.am_data['tags'] = tags
                    st.session_state.am_data['emotional_tags'] = emotional_tags
                    analyzed = True
                except Exception as e:
                    tag_error = f"Tagging failed: {e}"
            else:
                tag_error = "Please enter a reflection before analyzing."
        if tags or emotional_tags:
            st.markdown(f"<b>Themes:</b> {', '.join(tags) if tags else '—'}", unsafe_allow_html=True)
            st.markdown(f"<b>Emotions:</b> {', '.join(emotional_tags) if emotional_tags else '—'}", unsafe_allow_html=True)
        if tag_error:
            st.error(tag_error)
        elif analyzed:
            st.success("Tags and emotions updated!")
        st.session_state.am_data['reflection'] = reflection
        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="am_back_reflection")
        with col2:
            st.button("Next →", on_click=next_step, key="am_next_reflection")
    elif page == 'am_sleep_energy':
        st.header("☀️ AM Journal — Sleep & Energy")
        st.caption("Log your sleep and energy for the morning.")
        sleep_hours = st.number_input(
            "Hours of sleep:", min_value=0.0, max_value=12.0,
            value=st.session_state.am_data.get('sleep_hours', 7.0), step=0.5, key="am_sleep_hours")
        sleep_quality = st.slider(
            "Sleep Quality (1–10):", 1, 10,
            value=st.session_state.am_data.get('sleep_quality', 7), key="am_sleep_quality")
        energy_score = st.slider(
            "Morning Energy (1–10):", 1, 10,
            value=st.session_state.am_data.get('energy_score', 5), key="am_energy_score")
        st.session_state.am_data['sleep_hours'] = sleep_hours
        st.session_state.am_data['sleep_quality'] = sleep_quality
        st.session_state.am_data['energy_score'] = energy_score
        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="am_back_sleep_energy")
        with col2:
            st.button("Next →", on_click=next_step, key="am_next_sleep_energy")
    elif page == 'am_intentions':
        st.header("☀️ AM Journal — Intentions & Purpose")
        st.caption("Set your intentions and confirm your purpose for today.")
        intentions = st.text_area(
            "Today's Intentions",
            value=st.session_state.am_data.get('intentions', ''),
            height=100,
            key="am_intentions_text"
        )
        purpose_confirmed = st.checkbox(
            "I have reflected on my purpose for today.",
            value=st.session_state.am_data.get('purpose_confirmed', False),
            key="am_purpose_confirmed")
        st.session_state.am_data['intentions'] = intentions
        st.session_state.am_data['purpose_confirmed'] = purpose_confirmed
        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="am_back_intentions")
        with col2:
            st.button("Next →", on_click=next_step, key="am_next_intentions")
    elif page == 'am_diagnostics':
        st.header("☀️ AM Journal — Diagnostics & Summary Preview")
        st.caption("Review AI-powered diagnostics and confirm before saving your entry.")
        import llm_service
        from datetime import datetime
        journal_log = dict(st.session_state.am_data)
        recent_logs = []
        try:
            # Load recent AM logs for context (optional)
            import glob
            for fname in sorted(glob.glob('vesper-archive/am_log_*.json'), reverse=True)[:3]:
                with open(fname, 'r') as f:
                    recent_logs.append(json.load(f))
        except Exception:
            pass
        # Run diagnostics
        diagnostics = []
        try:
            diagnostics = llm_service.run_journal_diagnostics(journal_log, recent_logs, instruction_set=None)
        except Exception as e:
            diagnostics = [f"Diagnostics failed: {e}"]
        if diagnostics:
            st.warning("\n".join(diagnostics))
        else:
            st.success("No major issues detected. Ready to save!")
        st.markdown("---")
        st.markdown(f"**Reflection:** {journal_log.get('reflection','—')}")
        st.markdown(f"**Tags:** {', '.join(journal_log.get('tags', [])) or '—'}")
        st.markdown(f"**Emotions:** {', '.join(journal_log.get('emotional_tags', [])) or '—'}")
        st.markdown(f"**Sleep:** {journal_log.get('sleep_hours','—')}h, Quality: {journal_log.get('sleep_quality','—')}/10")
        st.markdown(f"**Energy:** {journal_log.get('energy_score','—')}/10")
        st.markdown(f"**Intentions:** {journal_log.get('intentions','—')}")
        st.markdown(f"**Purpose Confirmed:** {'✅' if journal_log.get('purpose_confirmed') else '❌'}")
        col1, col2 = st.columns(2)
        with col1:
            st.button("← Back", on_click=prev_step, key="am_back_diagnostics")
        with col2:
            if st.button("Finish AM Routine & Save", key="am_finish"):
                try:
                    am_entry = {
                        "timestamp": "2025-07-18T10:05:11-04:00",
                        **st.session_state.am_data
                    }
                    os.makedirs("vesper-archive", exist_ok=True)
                    with open(f"vesper-archive/am_log_20250718.json", "w") as f:
                        json.dump(am_entry, f, indent=2)
                    st.success("✅ Morning reflection saved!")
                    st.balloons()
                    st.session_state.journal_page = 'am_complete'
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save AM log: {e}")
    elif page == 'am_complete':
        st.header("☀️ AM Journal — Complete!")
        st.success("Your AM reflection has been saved. Have a great day!")
        if st.button("Start New AM Routine", key="am_restart"):
            st.session_state.journal_page = steps[0]
            st.session_state.am_data = {}
            st.rerun()

def workout_tracker():
    """Workout tracking with improved navigation and sectioned flow"""
    st.header("💪 Workout Tracker")
    import json
    # --- Section Switcher ---
    tracker_tabs = ["Workout Flow", "Custom Workout"]
    tracker_section = st.radio("Select Section", tracker_tabs, horizontal=True, key="workout_tracker_tabs")
    if tracker_section == "Custom Workout":
        st.subheader("🛠️ Custom Workout Creator")
        if 'custom_workout' not in st.session_state:
            st.session_state.custom_workout = {
                "name": "My Custom Workout",
                "supersets": []
            }
        cw = st.session_state.custom_workout
        cw['name'] = st.text_input("Workout Name", cw.get('name', 'My Custom Workout'))
        # Supersets
        st.markdown("### Supersets")
        superset_count = len(cw['supersets'])
        add_superset = st.button("Add Superset")
        if add_superset:
            cw['supersets'].append({"name": f"Superset {superset_count+1}", "exercises": []})
        for idx, superset in enumerate(cw['supersets']):
            with st.expander(f"Superset {idx+1}: {superset['name']}", expanded=True):
                superset['name'] = st.text_input(f"Superset Name", value=superset['name'], key=f"ss_name_{idx}")
                # Exercises
                st.markdown("#### Exercises")
                for ex_idx, ex in enumerate(superset['exercises']):
                    col1, col2, col3, col4 = st.columns([3,2,2,1])
                    with col1:
                        ex['name'] = st.text_input(f"Exercise Name", value=ex.get('name',''), key=f"ex_name_{idx}_{ex_idx}")
                    with col2:
                        ex['sets'] = st.text_input(f"Sets", value=ex.get('sets',''), key=f"ex_sets_{idx}_{ex_idx}")
                    with col3:
                        ex['reps'] = st.text_input(f"Reps", value=ex.get('reps',''), key=f"ex_reps_{idx}_{ex_idx}")
                    with col4:
                        if st.button("❌", key=f"del_ex_{idx}_{ex_idx}"):
                            superset['exercises'].pop(ex_idx)
                            st.experimental_rerun()
                    ex['notes'] = st.text_area(f"Notes", value=ex.get('notes',''), key=f"ex_notes_{idx}_{ex_idx}")
                if st.button("Add Exercise", key=f"add_ex_{idx}"):
                    superset['exercises'].append({"name":"","sets":"","reps":"","notes":""})
                    st.experimental_rerun()
                if st.button("Remove Superset", key=f"del_ss_{idx}"):
                    cw['supersets'].pop(idx)
                    st.experimental_rerun()
        # Save/download
        st.markdown("---")
        st.success("Your custom workout is saved in this session.")
        st.download_button("Download as JSON", json.dumps(cw, indent=2), file_name="custom_workout.json")
        st.info("You can now use this template for your own workout sessions!")
        return
    # --- Default Workout Flow ---
    # Initialize workout session state
    if 'workout_section' not in st.session_state:
        st.session_state.workout_section = 'pre_workout'
    if 'workout_data' not in st.session_state:
        st.session_state.workout_data = {}
    
    section = st.session_state.workout_section
    if section == 'pre_workout':
        st.subheader("Pre-Workout Check-In")
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
            st.info("**Recovery Framework**\n1 = sore/fatigued\n5 = average\n10 = fully recovered")
            pre_recovery = st.slider("Recovery (1-10)", 1, 10, 
                                   st.session_state.workout_data.get('pre_recovery', 5), key="pre_recovery")
        if st.button("Start Workout", key="start_workout"):
            st.session_state.workout_section = 'main_workout'
            st.session_state.workout_data['pre_energy'] = pre_energy
            st.session_state.workout_data['pre_mood'] = pre_mood
            st.session_state.workout_data['pre_recovery'] = pre_recovery
            st.rerun()
    elif section == 'main_workout':
        st.subheader("Supersets")
        # Individual Superset Navigation
        supersets = workout_plan.get('supersets', [])
        if 'current_superset_idx' not in st.session_state:
            st.session_state.current_superset_idx = 0
        idx = st.session_state.current_superset_idx
        num_supersets = len(supersets)
        if num_supersets == 0:
            st.info("No supersets in this workout. You can proceed to post-workout review.")
            if st.button("Next: Post-Workout", key="no_supersets_next"):
                st.session_state.workout_section = 'post_workout'
                st.rerun()
        else:
            superset = supersets[idx]
            st.markdown(f"### Superset {idx+1} of {num_supersets}: {superset.get('name', f'Superset {idx+1}')}")
            log_key = f"superset_log_{idx}"
            if log_key not in st.session_state:
                st.session_state[log_key] = {ex['name']: {"sets": "", "reps": "", "completed": False, "notes": ""} for ex in superset.get('exercises',[])}
            for ex in superset.get('exercises', []):
                st.write(f"**{ex['name']}**")
                col1, col2, col3 = st.columns([2,2,3])
                with col1:
                    st.session_state[log_key][ex['name']]['sets'] = st.text_input(f"Sets ({ex['name']})", value=st.session_state[log_key][ex['name']]['sets'], key=f"sets_{idx}_{ex['name']}")
                with col2:
                    st.session_state[log_key][ex['name']]['reps'] = st.text_input(f"Reps ({ex['name']})", value=st.session_state[log_key][ex['name']]['reps'], key=f"reps_{idx}_{ex['name']}")
                with col3:
                    st.session_state[log_key][ex['name']]['completed'] = st.checkbox(f"Completed ({ex['name']})", value=st.session_state[log_key][ex['name']]['completed'], key=f"done_{idx}_{ex['name']}")
                st.session_state[log_key][ex['name']]['notes'] = st.text_area(f"Notes ({ex['name']})", value=st.session_state[log_key][ex['name']]['notes'], key=f"notes_{idx}_{ex['name']}")
            col_prev, col_next = st.columns([1,1])
            with col_prev:
                if idx > 0 and st.button("", key="prev_superset"):
                    st.session_state.current_superset_idx -= 1
                    st.rerun()
            with col_next:
                if idx < num_supersets - 1 and st.button("Next Superset ", key="next_superset"):
                    st.session_state.current_superset_idx += 1
                    st.rerun()
                elif idx == num_supersets - 1 and st.button("Next: Post-Workout", key="next_post_workout"):
                    st.session_state.workout_section = 'post_workout'
                    st.session_state.current_superset_idx = 0
                    st.rerun()
                    st.session_state[log_key] = {ex['name']: {"sets": "", "reps": "", "completed": False, "notes": ""} for ex in superset.get('exercises',[])}
                for ex in superset.get('exercises', []):
                    st.write(f"**{ex['name']}**")
                    col1, col2, col3 = st.columns([2,2,3])
                    with col1:
                        st.session_state[log_key][ex['name']]['sets'] = st.text_input(f"Sets ({ex['name']})", value=st.session_state[log_key][ex['name']]['sets'], key=f"sets_{idx}_{ex['name']}")
                    with col2:
                        st.session_state[log_key][ex['name']]['reps'] = st.text_input(f"Reps ({ex['name']})", value=st.session_state[log_key][ex['name']]['reps'], key=f"reps_{idx}_{ex['name']}")
                    with col3:
                        st.session_state[log_key][ex['name']]['completed'] = st.checkbox(f"Completed ({ex['name']})", value=st.session_state[log_key][ex['name']]['completed'], key=f"done_{idx}_{ex['name']}")
                    st.session_state[log_key][ex['name']]['notes'] = st.text_area(f"Notes ({ex['name']})", value=st.session_state[log_key][ex['name']]['notes'], key=f"notes_{idx}_{ex['name']}")
                col_prev, col_next = st.columns([1,1])
                with col_prev:
                    if idx > 0 and st.button("⬅️ Previous Superset", key="prev_superset"):
                        st.session_state.current_superset_idx -= 1
                        st.rerun()
                with col_next:
                    if idx < num_supersets - 1 and st.button("Next Superset ➡️", key="next_superset"):
                        st.session_state.current_superset_idx += 1
                        st.rerun()
                    elif idx == num_supersets - 1 and st.button("Next: Post-Workout", key="next_post_workout"):
                        st.session_state.workout_section = 'post_workout'
                        st.session_state.current_superset_idx = 0
                        st.rerun()
    elif section == 'post_workout':
        st.subheader("Post-Workout Check-In")
        # ... post-workout UI ...
        if st.button("Finish Workout", key="finish_workout"):
            st.session_state.workout_section = 'review'
            st.rerun()
    elif section == 'review':
        st.subheader("Workout Review & Feedback")
        # --- LLM Workout Feedback ---
        workout_log = "Previous week's workout log goes here."
        if st.button("Get Feedback with GPT", key="workout_feedback_llm"):
            with st.spinner("Getting feedback via ChatGPT..."):
                feedback = llm_service.get_workout_feedback(workout_log)
                st.info(feedback)
        if st.button("Back to Landing", key="workout_landing"):
            st.session_state.workout_section = 'pre_workout'
            st.rerun()

def macro_tracking():
    """Macro tracking with mobile-optimized OCR support"""
    st.header("🍎 Macro Tracking")
    
    user_config = st.session_state.get('user_journal_config', {})
    toggles = user_config.get('toggles', {}) if user_config else {}
    meal_planning_enabled = toggles.get('macro_meal_planning', True)
    macro_tabs = ["📊 Macro Cheat Sheet", "📱 Label Scanner (Image/OCR)", "💬 Macro Chatbot", "🛒 Grocery List"]
    if meal_planning_enabled:
        macro_tabs.append("📖 Meal Planning")
    tab1, tab2, tab3, tab4, *tab5 = st.tabs(macro_tabs)

    # Macro Cheat Sheet (unchanged)
    with tab1:
        st.info("Quick macro reference for common foods.")
        import pandas as pd
        common_foods_data = [
            {"Name": "Chicken breast", "Category": "Protein", "Serving Size": "100g", "Calories": 165, "Protein (g)": 23, "Carbs (g)": 0, "Fat (g)": 3.6},
        ]
        df = pd.DataFrame(common_foods_data)
        st.dataframe(df)
        st.caption("Based on standard US nutrition guidelines.")

    # Label Scanner (Image/OCR)
    with tab2:
        st.info("Upload a nutrition label image, extract with OCR, or enter/edit manually. Confirm to log macros for your meal.")
        if 'macro_log' not in st.session_state:
            st.session_state.macro_log = []
        import pandas as pd
        from PIL import Image
        import tesserocr
        # Image upload and OCR
        import re
        uploaded_image = st.file_uploader("Upload Nutrition Label Image", type=["png", "jpg", "jpeg"])
        ocr_text = ""
        ocr_macros = {}
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Label", use_column_width=True)
            if st.button("Extract Text with OCR"):
                with st.spinner("Extracting text..."):
                    ocr_text = tesserocr.image_to_text(image)
                    st.session_state['ocr_text'] = ocr_text
                    # Try to parse macros
                    def extract_macro(pattern, text, cast=float, default=0):
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            try:
                                return cast(match.group(1))
                            except Exception:
                                return default
                        return default
                    macros = {
                        'Calories': extract_macro(r'calories\s*:?\s*(\d+)', ocr_text, int, 0),
                        'Protein (g)': extract_macro(r'protein\s*:?\s*(\d+(?:\.\d+)?)', ocr_text),
                        'Carbs (g)': extract_macro(r'carbohydrate[s]?\s*:?\s*(\d+(?:\.\d+)?)', ocr_text),
                        'Fat (g)': extract_macro(r'fat\s*:?\s*(\d+(?:\.\d+)?)', ocr_text),
                    }
                    st.session_state['ocr_macros'] = macros
            if 'ocr_text' in st.session_state:
                ocr_text = st.session_state['ocr_text']
                st.text_area("Extracted Text", value=ocr_text, height=120)
                # Show extracted macros if present
                if 'ocr_macros' in st.session_state:
                    st.markdown("**Auto-filled from OCR:**")
                    st.json(st.session_state['ocr_macros'])
                    ocr_macros = st.session_state['ocr_macros']
        # Macro entry form (manual or copy from OCR)
        with st.form("macro_label_form", clear_on_submit=True):
            item_name = st.text_input("Item Name", value=st.session_state.get('edit_item_name', ''))
            serving_size = st.text_input("Serving Size (e.g. 100g, 1 cup)", value=st.session_state.get('edit_serving_size', ''))
            calories = st.number_input("Calories", min_value=0, max_value=2000, step=1, value=st.session_state.get('edit_calories', ocr_macros.get('Calories', 0)))
            protein = st.number_input("Protein (g)", min_value=0.0, max_value=200.0, step=0.1, value=st.session_state.get('edit_protein', ocr_macros.get('Protein (g)', 0.0)))
            carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=200.0, step=0.1, value=st.session_state.get('edit_carbs', ocr_macros.get('Carbs (g)', 0.0)))
            fat = st.number_input("Fat (g)", min_value=0.0, max_value=100.0, step=0.1, value=st.session_state.get('edit_fat', ocr_macros.get('Fat (g)', 0.0)))
            submitted = st.form_submit_button("Confirm Macros")
            if submitted:
                entry = {
                    "Item": item_name,
                    "Serving Size": serving_size,
                    "Calories": calories,
                    "Protein (g)": protein,
                    "Carbs (g)": carbs,
                    "Fat (g)": fat
                }
                if st.session_state.get('edit_index') is not None:
                    st.session_state.macro_log[st.session_state.edit_index] = entry
                    st.success(f"Updated macros for: {item_name}")
                    st.session_state.edit_index = None
                else:
                    st.session_state.macro_log.append(entry)
                    st.success(f"Added macros for: {item_name}")
                for k in ['edit_item_name','edit_serving_size','edit_calories','edit_protein','edit_carbs','edit_fat','edit_index','ocr_text']:
                    if k in st.session_state:
                        del st.session_state[k]
        if st.session_state.macro_log:
            st.markdown("#### Logged Macro Entries")
            macro_df = pd.DataFrame(st.session_state.macro_log)
            for i, row in macro_df.iterrows():
                cols = st.columns([2,2,2,2,2,2,1,1])
                cols[0].write(row['Item'])
                cols[1].write(row['Serving Size'])
                cols[2].write(row['Calories'])
                cols[3].write(row['Protein (g)'])
                cols[4].write(row['Carbs (g)'])
                cols[5].write(row['Fat (g)'])
                if cols[6].button("✏️ Edit", key=f"edit_macro_{i}"):
                    st.session_state['edit_item_name'] = row['Item']
                    st.session_state['edit_serving_size'] = row['Serving Size']
                    st.session_state['edit_calories'] = row['Calories']
                    st.session_state['edit_protein'] = row['Protein (g)']
                    st.session_state['edit_carbs'] = row['Carbs (g)']
                    st.session_state['edit_fat'] = row['Fat (g)']
                    st.session_state['edit_index'] = i
                if cols[7].button("🗑️ Delete", key=f"delete_macro_{i}"):
                    st.session_state.macro_log.pop(i)
                    st.experimental_rerun()

    # Macro Chatbot (ChatGPT-style conversational)
    with tab3:
        st.info("Chat with the Macro Chatbot: describe your meals, ask questions, and let the assistant estimate macros. Your chat history is saved for this session.")
        if 'macro_chat_history' not in st.session_state:
            st.session_state.macro_chat_history = []  # List of {'role': 'user'/'assistant', 'content': str}
        if 'macro_log' not in st.session_state:
            st.session_state.macro_log = []

        # Chat history display
        for msg in st.session_state.macro_chat_history:
            if msg['role'] == 'user':
                st.markdown(f"<div style='background:#dbeafe;padding:8px 12px;border-radius:10px;max-width:90%;margin-bottom:4px;align-self:flex-end;text-align:right'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#f1f5f9;padding:8px 12px;border-radius:10px;max-width:90%;margin-bottom:4px;align-self:flex-start'><b>MacroBot:</b> {msg['content']}</div>", unsafe_allow_html=True)

        st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)
        col1, col2 = st.columns([4,1])
        with col1:
            user_input = st.text_input("Type your meal description or question...", key="macro_chat_input", value="")
        with col2:
            send_clicked = st.button("Send", key="macro_chat_send")
        clear_clicked = st.button("Clear Chat", key="macro_chat_clear")
        if clear_clicked:
            st.session_state.macro_chat_history = []
            st.experimental_rerun()
        if send_clicked and user_input.strip():
            # Add user message
            st.session_state.macro_chat_history.append({'role': 'user', 'content': user_input.strip()})
            # Compose context for LLM
            context_msgs = st.session_state.macro_chat_history[-8:]  # last 8 messages for context
            messages = [{"role": m['role'], "content": m['content']} for m in context_msgs]
            import openai, os, json
            api_key = os.getenv("OPENAI_API_KEY") or (hasattr(openai, 'api_key') and openai.api_key)
            if not api_key:
                st.session_state.macro_chat_history.append({'role': 'assistant', 'content': "[Error: OpenAI API key not set]"})
            else:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4-turbo",
                        messages=[{"role": "system", "content": "You are MacroBot, a helpful nutrition assistant. Estimate macros for described foods, answer nutrition questions, and always return macro estimates as JSON if possible."}] + messages,
                        temperature=0.3,
                        max_tokens=300
                    )
                    reply = response['choices'][0]['message']['content']
                    st.session_state.macro_chat_history.append({'role': 'assistant', 'content': reply})
                except Exception as e:
                    st.session_state.macro_chat_history.append({'role': 'assistant', 'content': f"[Error: {e}]"})
            st.experimental_rerun()

        # Macro extraction and confirmation UI (scan all assistant messages for macro JSON)
        import re, json
        found_macros = []
        for msg in st.session_state.macro_chat_history:
            if msg['role'] == 'assistant':
                # Try to extract macro JSON from message
                try:
                    match = re.search(r'\{[^\}]+"Calories"[^\}]+\}', msg['content'], re.DOTALL)
                    if match:
                        macros = json.loads(match.group(0))
                        if all(k in macros for k in ["Calories","Protein (g)","Carbs (g)","Fat (g)"]):
                            found_macros.append(macros)
                except Exception:
                    continue
        if found_macros:
            st.markdown("**Macros found in chat:**")
            for i, macros in enumerate(found_macros):
                with st.expander(f"Macros suggestion #{i+1}"):
                    st.json(macros)
                    with st.form(f"confirm_macro_{i}", clear_on_submit=True):
                        item_name = st.text_input("Item Name (optional)", key=f"macro_item_{i}")
                        serving_size = st.text_input("Serving Size (optional)", key=f"macro_serving_{i}")
                        calories = st.number_input("Calories", min_value=0, max_value=2000, step=1, value=int(macros["Calories"]), key=f"macro_cal_{i}")
                        protein = st.number_input("Protein (g)", min_value=0.0, max_value=200.0, step=0.1, value=float(macros["Protein (g)"]), key=f"macro_prot_{i}")
                        carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=200.0, step=0.1, value=float(macros["Carbs (g)"]), key=f"macro_carb_{i}")
                        fat = st.number_input("Fat (g)", min_value=0.0, max_value=100.0, step=0.1, value=float(macros["Fat (g)"]), key=f"macro_fat_{i}")
                        confirm = st.form_submit_button("Add to Macro Log")
                        if confirm:
                            entry = {
                                "Item": item_name,
                                "Serving Size": serving_size,
                                "Calories": calories,
                                "Protein (g)": protein,
                                "Carbs (g)": carbs,
                                "Fat (g)": fat
                            }
                            st.session_state.macro_log.append(entry)
                            st.success("Added macros from chat!")

    # Grocery List and Meal Planning tabs (unchanged)
    # ... (existing code for tab4, tab5, etc.).pop(i)
                    st.experimental_rerun()

    with tab4:
        st.info("Plan meals, substitutions, and get meal ideas based on your pantry and preferences. Chat with MealBot to get suggestions or advice!")
        # --- Editable Pantry ---
        if 'pantry_items' not in st.session_state:
            st.session_state.pantry_items = [
                "Chicken breast", "Eggs", "Spinach", "Feta cheese", "Ground beef", "Rice", "Tomato"
            ]
        st.subheader("🗃️ Your Pantry")
        # Pantry editor
        pantry_str = st.text_area("Edit your pantry list (one item per line):", '\n'.join(st.session_state.pantry_items), height=100)
        if pantry_str:
            st.session_state.pantry_items = [item.strip() for item in pantry_str.splitlines() if item.strip()]
        col_add, col_remove = st.columns([2,1])
        with col_add:
            new_item = st.text_input("Add an ingredient:", key="add_pantry_item")
            if st.button("Add", key="add_pantry_btn") and new_item:
                if new_item not in st.session_state.pantry_items:
                    st.session_state.pantry_items.append(new_item)
                    st.success(f'Added: {new_item}')
        with col_remove:
            remove_item = st.selectbox("Remove ingredient:", ["-"] + st.session_state.pantry_items, key="remove_pantry_item")
            if remove_item != "-" and st.button("Remove", key="remove_pantry_btn"):
                st.session_state.pantry_items = [i for i in st.session_state.pantry_items if i != remove_item]
                st.info(f'Removed: {remove_item}')
        meal_type = st.selectbox("Meal type", ["breakfast", "lunch", "dinner"], index=2)
        st.write("**Current Pantry:**", ', '.join(st.session_state.pantry_items))

        # --- Meal Planning Chat (ChatGPT-style) ---
        meal_chat_key = "meal_planning_chat"
        if meal_chat_key not in st.session_state:
            st.session_state[meal_chat_key] = []  # {'role': 'user'/'assistant', 'content': str}
        st.markdown("---")
        st.header("🍽️ Meal Planning Chat")
        st.caption("Ask for meal ideas, substitutions, or planning advice. Your chat history is saved for this session.")
        for msg in st.session_state[meal_chat_key]:
            if msg['role'] == 'user':
                st.markdown(f"<div style='background:#dbeafe;padding:8px 12px;border-radius:10px;max-width:90%;margin-bottom:4px;align-self:flex-end;text-align:right'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#f1f5f9;padding:8px 12px;border-radius:10px;max-width:90%;margin-bottom:4px;align-self:flex-start'><b>MealBot:</b> {msg['content']}</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)
        col1, col2 = st.columns([4,1])
        with col1:
            meal_user_input = st.text_input("Type your meal planning question or request...", key="meal_chat_input", value="")
        with col2:
            meal_send_clicked = st.button("Send", key="meal_chat_send")
        meal_clear_clicked = st.button("Clear Chat", key="meal_chat_clear")
        if meal_clear_clicked:
            st.session_state[meal_chat_key] = []
            st.experimental_rerun()
        if meal_send_clicked and meal_user_input.strip():
            st.session_state[meal_chat_key].append({'role': 'user', 'content': meal_user_input.strip()})
            # Compose context for LLM
            context_msgs = st.session_state[meal_chat_key][-8:]
            messages = [{"role": m['role'], "content": m['content']} for m in context_msgs]
            import openai, os
            api_key = os.getenv("OPENAI_API_KEY") or (hasattr(openai, 'api_key') and openai.api_key)
            if not api_key:
                st.session_state[meal_chat_key].append({'role': 'assistant', 'content': "[Error: OpenAI API key not set]"})
            else:
                # Compose pantry and meal type for context
                pantry_context = ', '.join(st.session_state.pantry_items)
                system_prompt = f"You are MealBot, a helpful meal planning assistant. The user's current pantry is: {pantry_context}. They are planning a {meal_type}. Suggest meal ideas, substitutions, or answer questions. Return meal suggestions as a markdown list if possible."
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4-turbo",
                        messages=[{"role": "system", "content": system_prompt}] + messages,
                        temperature=0.3,
                        max_tokens=400
                    )
                    reply = response['choices'][0]['message']['content']
                    st.session_state[meal_chat_key].append({'role': 'assistant', 'content': reply})
                except Exception as e:
                    st.session_state[meal_chat_key].append({'role': 'assistant', 'content': f"[Error: {e}]"})
            st.experimental_rerun()

def llm_service():
    # ... (your LLM service implementation here)
    pass

def check_journal_surface(reflection):
    # ... (your implementation here)
    pass

def tag_journal_entry(reflection):
    """
    Use the hierarchical tagging engine to extract and display tags for a journal reflection.
    Returns (tag_tree, flat_tag_list).
    """
    from arcana_scrolls.tagging_engine import gpt_generate_tags, build_tag_tree, flatten_tag_tree
    tags = gpt_generate_tags(reflection)
    tag_tree = build_tag_tree(tags)
    flat_tag_list = flatten_tag_tree(tag_tree)
    return tag_tree, flat_tag_list

def auto_score_pm_metrics(reflection, relationships, metrics):
    """
    Use LLM to auto-score PM metrics based on both reflection and relationships text.
    Returns a dict of {metric: score}.
    """
    import openai
    import os
    import json
    api_key = os.getenv("OPENAI_API_KEY") or (hasattr(openai, 'api_key') and openai.api_key)
    if not api_key:
        raise RuntimeError("OpenAI API key not set in environment or openai.api_key")
    prompt = f"""
    Given the following evening journal reflection and relationship notes, score each metric from 1 to 10 (10 = excellent, 1 = poor) based on the user's state. Return a JSON object mapping each metric to its score. Only use the metrics provided and do not invent new ones.

    Reflection:
    {reflection}

    Relationships:
    {relationships}

    Metrics: {', '.join(metrics)}

    Output format:
    {{"metric1": score, "metric2": score, ...}}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant for journaling diagnostics."},
                      {"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=256
        )
        content = response['choices'][0]['message']['content']
        # Extract JSON from response
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            content = content[start:end]
        result = json.loads(content)
        # Ensure only metrics in the input list are returned
        return {k: int(v) for k, v in result.items() if k in metrics}
    except Exception as e:
        return {m: 5 for m in metrics}  # Default to neutral scores if error

def analyze_trends(logs):
    # ... (your implementation here)
    pass

def get_workout_feedback(workout_log):
    # ... (your implementation here)
    pass

def analyze_macros(macro_query):
    # ... (your implementation here)
    pass

def get_meal_suggestions(pantry, meal_type):
    # ... (your implementation here)
    pass

def diagnostics():
    tab1, tab2 = st.tabs(["📊 System Check", "📝 Validation"])
    
    with tab1:
        st.info("Check system status and required directories.")
        required_dirs = ["vesper-archive", "kinetica-forge"]
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
    
    user_config = st.session_state.get('user_journal_config')
    export_enabled = user_config and user_config.get('toggles', {}).get('export', False)
    if export_enabled:
        tab1, tab2, tab3, tab4 = st.tabs(["🔑 API Keys", "👤 Preferences", "📖 About", "⬇️ Export"])
    else:
        tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "👤 Preferences", "📖 About"])
    
    with tab1:
        st.info("Configure API keys and external services.")
        st.warning("⚠️ Use the Secrets tab in Replit to set sensitive values securely.")
        
        # OpenAI API Key Management (runtime + env/secrets)
        session_key = st.session_state.get('openai_api_key')
        env_key = get_secret('OPENAI_API_KEY')
        if session_key:
            st.success('OpenAI API Key: ✅ Set (Session)')
        elif env_key:
            st.success('OpenAI API Key: ✅ Set (Env/Secrets)')
        else:
            st.warning('OpenAI API Key: ❌ Not set')

        with st.form('openai_key_form'):
            st.write('Enter your OpenAI API key below. This will only be stored for your session and is never logged or saved to disk.')
            new_key = st.text_input('OpenAI API Key', type='password', value=session_key or '', help='Paste your OpenAI API key here. Session-only.')
            submitted = st.form_submit_button('Save Key')
            if submitted:
                if new_key and new_key.startswith('sk-'):
                    st.session_state['openai_api_key'] = new_key
                    st.success('OpenAI API Key saved for this session!')
                elif new_key:
                    st.error('Invalid key format. Should start with sk-')
                else:
                    st.session_state.pop('openai_api_key', None)
                    st.info('Key cleared from session.')

        # Display status for other secrets
        secrets_to_check = ["APP_PASSWORD"]
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

    with tab4:
        st.header("⬇️ Export Journaling, Macro, and Workout Data")
        import glob
        import json
        # Export PM/AM logs
        am_logs = sorted(glob.glob("vesper-archive/am_log_*.json"))
        # Export config
        st.markdown("---")
        if os.path.exists('user_journal_config.json'):
            config_content = load_json('user_journal_config.json')
            st.download_button("Download Journal Config (JSON)", config_content, file_name="user_journal_config.json")
        st.info("You can also export logs as Markdown from the Diagnostics or Workout Tracker pages. All logs and config are downloadable for backup or analysis. Mobile optimized.")

    if export_enabled:
        with tab4:
            # ... (rest of the code remains the same)
            st.markdown("""
                <div style='background: linear-gradient(90deg,#f0f4f8 60%,#e3f2fd 100%); padding: 1.5em 1.2em 1.2em 1.2em; border-radius: 15px; margin-bottom: 2em;'>
            """, unsafe_allow_html=True)

            st.header("⬇️ Export Journaling, Macro, and Workout Data")
            st.info("""
Export all your logs and configuration for backup, analysis, or migration.
- **Tap and hold** download buttons on mobile to save files.
- Markdown export is available in Diagnostics and Workout Tracker.
- All buttons are mobile-optimized for easy access.
""")
            import glob
            import json
            am_logs = sorted(glob.glob("vesper-archive/am_log_*.json"))
            pm_logs = sorted(glob.glob("vesper-archive/pm_log_*.json"))
            macro_logs = sorted(glob.glob("macro_log_*.json"))
            workout_logs = sorted(glob.glob("workout_log_*.json"))
            def download_button_for_file(path):
                with open(path) as f:
                    content = f.read()
                st.download_button(f"Download {os.path.basename(path)}", content, file_name=os.path.basename(path), use_container_width=True)
            # --- AM Logs ---
            st.markdown("""
                <div style='position:sticky;top:0.5em;z-index:2;background:#f0f4f8;padding:0.4em 0.7em 0.2em 0.7em;border-radius:8px;margin-bottom:0.5em;'>
                <b>AM Logs</b> <span style='color:#1976d2;font-size:0.97em;'>(%d available)</span>
                </div>""" % len(am_logs), unsafe_allow_html=True)
            for path in am_logs:
                download_button_for_file(path)
            st.markdown("<hr style='border:0;border-top:1.5px solid #e3e3e3;margin:1.3em 0;'>", unsafe_allow_html=True)
            # --- PM Logs ---
            st.markdown("""
                <div style='position:sticky;top:0.5em;z-index:2;background:#f0f4f8;padding:0.4em 0.7em 0.2em 0.7em;border-radius:8px;margin-bottom:0.5em;'>
                <b>PM Logs</b> <span style='color:#1976d2;font-size:0.97em;'>(%d available)</span>
                </div>""" % len(pm_logs), unsafe_allow_html=True)
            for path in pm_logs:
                download_button_for_file(path)
            st.markdown("<hr style='border:0;border-top:1.5px solid #e3e3e3;margin:1.3em 0;'>", unsafe_allow_html=True)
            # --- Macro Logs ---
            st.markdown("""
                <div style='position:sticky;top:0.5em;z-index:2;background:#f0f4f8;padding:0.4em 0.7em 0.2em 0.7em;border-radius:8px;margin-bottom:0.5em;'>
                <b>Macro Logs</b> <span style='color:#1976d2;font-size:0.97em;'>(%d available)</span>
                </div>""" % len(macro_logs), unsafe_allow_html=True)
            for path in macro_logs:
                download_button_for_file(path)
            st.markdown("<hr style='border:0;border-top:1.5px solid #e3e3e3;margin:1.3em 0;'>", unsafe_allow_html=True)
            # --- Workout Logs ---
            st.markdown("""
                <div style='position:sticky;top:0.5em;z-index:2;background:#f0f4f8;padding:0.4em 0.7em 0.2em 0.7em;border-radius:8px;margin-bottom:0.5em;'>
                <b>Workout Logs</b> <span style='color:#1976d2;font-size:0.97em;'>(%d available)</span>
                </div>""" % len(workout_logs), unsafe_allow_html=True)
            for path in workout_logs:
                download_button_for_file(path)
            st.markdown("""
                </div>
            """, unsafe_allow_html=True)
            st.info("You can also export logs as Markdown from the Diagnostics or Workout Tracker pages.")
    elif not export_enabled:
        st.warning("Export and download features are currently disabled in your configuration. To enable, turn on the Export toggle in Journal Setup.")


# --- Main application ---
def load_user_journal_config():
    import json
    if os.path.exists('user_journal_config.json'):
        try:
            return load_json('user_journal_config.json')
        except Exception as e:
            st.error(f"Failed to load config: {e}")
    return None

def main():
    """Main application entry point"""
    init_session_state()
    authenticate()
    
    # Load user config
    user_config = load_user_journal_config()
    st.session_state.user_journal_config = user_config
    
    # Main content area
    section = sidebar_navigation()
    
    # If config missing, prompt onboarding except for Journal Setup/Settings
    needs_onboarding = user_config is None and section not in ["Journal Setup", "Settings"]
    if needs_onboarding:
        st.warning("Please complete onboarding in Journal Setup before using LatticeFlow.")
        onboarding.run_onboarding()
        return
    
    # Show landing page or selected section
    if st.session_state.show_landing:
        landing_page()
    elif section == "AM Journal":
        am_journal(user_config)
    elif section == "PM Journal":
        pm_journal(user_config)
    elif section == "Workout Tracker":
        workout_tracker()
    elif section == "Macro Tracking":
        macro_tracking()
    elif section == "Memory Board":
        if user_config and user_config.get('toggles', {}).get('adhd', False):
            memory_board()
        else:
            st.info("Enable ADHD Toolkit in Journal Setup to use the Memory Board.")
    elif section == "ADHD Toolkit":
        if user_config and user_config.get('toggles', {}).get('adhd', False):
            adhd_toolkit()
        else:
            st.info("Enable ADHD Toolkit in Journal Setup to use the ADHD Toolkit.")
    elif section == "Diagnostics":
        diagnostics()
    elif section == "Journal Setup":
        onboarding.run_onboarding()
    elif section == "Settings":
        settings()

    # Hide modules not enabled in config
    # Sidebar: dynamically show/hide based on toggles
    # This is handled in sidebar_navigation()

    # Mobile polish: ensure all flows use mobile CSS (already applied globally)

    # All navigation is session-state-driven; journal_page, workout_page, etc. are set and respected throughout.

    # All modules and subfeatures are now pluggable/toggleable per user config.

    
    # Footer
    st.markdown("---")
    st.markdown("*LatticeFlow © 2025 | Built with Streamlit*")

if __name__ == "__main__":
    main()
