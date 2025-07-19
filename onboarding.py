import streamlit as st
import json
import os
import copy
import uuid
from beemind import load_adhd_scripts, load_memory_cards, save_memory_cards

# Supported types
SUPPORTED_TYPES = [
    "prompt", "metric", "checklist", "avoidance", "intention", "reflection", "exercise", "timer", "resource"
]
TYPE_DESCRIPTIONS = {
    "prompt": "Elicits a free-text reflection or answer.",
    "metric": "Quantifies something with a scale, number, or selection.",
    "checklist": "Check off one or more items from a list.",
    "avoidance": "Reminds you to avoid a specific behavior or thought pattern.",
    "intention": "Set or affirm an intention for the day/session.",
    "reflection": "Prompts you to look back on the day/session.",
    "exercise": "Specifies a physical activity to perform and track.",
    "timer": "Guides you to spend a set amount of time on an activity.",
    "resource": "Provides a link or resource for inspiration or instruction."
}

def run_onboarding():
    # Session state initialization
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'draft_am_routine' not in st.session_state:
        st.session_state.draft_am_routine = []
    if 'draft_pm_routine' not in st.session_state:
        st.session_state.draft_pm_routine = []
    if 'onboarding_config' not in st.session_state:
        st.session_state.onboarding_config = {}

    # Render chat history
    for i, (who, msg, _) in enumerate(st.session_state.chat_history):
                    emotion_profile["intensities"][i] = new_intensity
            st.session_state.routine_builder_emotion_profile = emotion_profile

        if st.button("Save Routine", key="routine_builder_save"):
            # Save routine to config (by type, e.g. am_routine)
            routine_type = st.session_state.routine_builder_routine_type
            final_config = {routine_type: copy.deepcopy(draft)}
            with open("user_journal_config.json", "w") as f:
                import json
                json.dump(final_config, f, indent=2)
        if who == "bot":
            st.markdown(f"<div style='background:#222;color:#fff;padding:0.7em 1em;border-radius:1em 1em 1em 0.2em;width:fit-content;margin-bottom:0.3em;'><b>🧑‍🏫 CoachBot:</b> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#e0e0e0;color:#222;padding:0.7em 1em;border-radius:1em 1em 0.2em 1em;width:fit-content;margin-left:auto;margin-bottom:0.3em;'><b>🙋 You:</b> {msg}</div>", unsafe_allow_html=True)

    # --- User input box ---
    user_input = st.text_input("Type your answer and press Enter:", key=f"onboard_input_{len(chat_history)}")
    if st.button("Send", key=f"onboard_send_{len(chat_history)}") and user_input.strip():
        chat_history.append(("user", user_input.strip()))
        # --- Step 0: Routine selection ---
        if onboarding_step == 0:
            answer = user_input.strip().lower()
            if "am" in answer and "pm" in answer:
                routine_choices['am'] = True
                routine_choices['pm'] = True
                chat_history.append(("bot", "Great! We’ll set up both AM and PM routines."))
                st.session_state.current_routine = 'am'
                st.session_state.onboarding_step = 1
                st.session_state.routine_element_idx = 0
            elif "am" in answer:
                routine_choices['am'] = True
                routine_choices['pm'] = False
                chat_history.append(("bot", "Great! We’ll set up your AM routine first."))
                st.session_state.current_routine = 'am'
                st.session_state.onboarding_step = 1
                st.session_state.routine_element_idx = 0
            elif "pm" in answer:
                routine_choices['am'] = False
                routine_choices['pm'] = True
                chat_history.append(("bot", "Great! We’ll set up your PM routine."))
                st.session_state.current_routine = 'pm'
                st.session_state.onboarding_step = 1
                st.session_state.routine_element_idx = 0
            else:
                chat_history.append(("bot", "Sorry, I didn’t understand. Would you like an AM routine, a PM routine, or both?"))
            st.session_state.chat_history = chat_history
            st.experimental_rerun()
            enabled = answers.get('features',{}).get(fname, False)
            st.markdown(f"- {ftitle}: {'✅ Enabled' if enabled else '❌ Disabled'}")
        st.info("You can always update these in Journal Setup or Settings.")
        if st.button("Save & Finish", key="onboard_save_final"):
            toggles = {fname: answers.get('features',{}).get(fname, False) for fname,_,_ in feature_list}
            # Style toggle
            toggles['style'] = 'dark' if toggles.get('style', False) else 'Light'
            final_config = {
                'domains': [d.strip() for d in answers.get('domains','').split(',') if d.strip()],
                'entities': [e.strip() for e in answers.get('entities','').split(',') if e.strip()],
                'metrics': [m.strip() for m in answers.get('metrics','').split(',') if m.strip()],
                'toggles': toggles
            }
            with open("user_journal_config.json", "w") as f:
                json.dump(final_config, f, indent=2)
            st.success("Configuration saved! You can edit this anytime in Journal Setup.")
            st.session_state.onboarding_config = final_config
            return

        st.markdown(f"**Domains:** {answers.get('domains','')}")
        st.markdown(f"**Entities:** {answers.get('entities','')}")
        st.markdown(f"**Metrics:** {answers.get('metrics','')}")
        st.markdown(f"**Features:** {answers.get('features','')}")
        review_input = st.text_input("Type 'ok' to confirm or 'edit' to change:", key="onboard_review_input")
        if review_input.strip().lower() == 'ok':
            # Save config and finish
            features = answers.get('features','')
            toggles = {
                'calendar': 'calendar' in features,
                'weather': 'weather' in features,
                'adhd': 'adhd' in features,
                'mantra': 'mantra' in features,
                'export': 'export' in features,
                'style': 'dark' if 'style=dark' in features else 'Light'
            }
            final_config = {
                'domains': [d.strip() for d in answers.get('domains','').split(',') if d.strip()],
                'entities': [e.strip() for e in answers.get('entities','').split(',') if e.strip()],
                'metrics': [m.strip() for m in answers.get('metrics','').split(',') if m.strip()],
                'toggles': toggles
            }
            with open("user_journal_config.json", "w") as f:
                json.dump(final_config, f, indent=2)
            st.success("Configuration saved! You can edit this anytime in Journal Setup.")
            st.session_state.onboarding_config = final_config
            return
        elif review_input.strip().lower() == 'edit':
            st.info("Please restart onboarding to change your answers.")
            return
        else:
            return

    # Only one input at a time for current question
    qkey = questions[step+1][2]
    user_input = st.text_input("Your answer:", key=f"onboard_input_{qkey}")

    
