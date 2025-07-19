import streamlit as st
import json
from json_persistence import load_json, atomic_save_json
import os
from beemind import load_adhd_scripts, load_memory_cards, save_memory_cards

GROCERY_LIST_PATH = "standard_grocery_list.json"
USER_GROCERY_PATH = "user_grocery_list.json"

# --- Utility Functions ---
def load_standard_grocery_list():
    return load_json(GROCERY_LIST_PATH, default=[])

def load_user_grocery_list():
    if not os.path.exists(USER_GROCERY_PATH):
        with open(USER_GROCERY_PATH, "w") as f:
            json.dump([], f)
    return load_json(USER_GROCERY_PATH, default=[])

def save_user_grocery_list(lst):
    atomic_save_json(USER_GROCERY_PATH, lst)

# --- Streamlit UI ---
def grocery_ui():
    st.title("Grocery List & Inventory")
    std_list = load_standard_grocery_list()
    user_list = load_user_grocery_list()

    st.header("Current Grocery List")
    for item in user_list:
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(item)
        with col2:
            if st.button("Remove", key=f"remove_{item}"):
                user_list.remove(item)
                save_user_grocery_list(user_list)
                st.experimental_rerun()
    st.write("---")
    new_item = st.text_input("Add Grocery Item")
    if st.button("Add Item") and new_item:
        user_list.append(new_item)
        save_user_grocery_list(user_list)
        st.experimental_rerun()

    # --- Voice Recording for Grocery Items ---
    st.subheader("Record Grocery Item (Voice)")
    audio_file = st.file_uploader("Upload audio file (WAV/MP3)", type=["wav", "mp3"], key="audio_upload")
    if audio_file is not None:
        st.audio(audio_file)
        # Stub: Replace this with Whisper API call
        def transcribe_audio_stub(audio_file):
            return "Stub transcription: Replace with Whisper API call."
        transcription = transcribe_audio_stub(audio_file)
        edited_transcription = st.text_input("Transcription (edit if needed)", value=transcription, key="voice_transcript")
        if st.button("Add Transcribed Item") and edited_transcription:
            user_list.append(edited_transcription)
            save_user_grocery_list(user_list)
            st.success(f"Added: {edited_transcription}")
            st.experimental_rerun()

    st.header("Standard Grocery List (Reference)")
    for item in std_list:
        st.write(f"- {item}")
    st.write("---")
    if st.button("Reset to Standard List"):
        save_user_grocery_list(std_list)
        st.success("Reset!")
        st.experimental_rerun()

if __name__ == "__main__":
    grocery_ui()
