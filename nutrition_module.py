import streamlit as st
import json
from json_persistence import load_json, atomic_save_json
import os
from beemind import load_adhd_scripts as beemind_load_adhd_scripts
from beemind import load_memory_cards as beemind_load_memory_cards
from beemind import save_memory_cards as beemind_save_memory_cards

RECIPES_PATH = "recipes.json"
MACRO_CHEATSHEET_PATH = "macro_cheatsheet.json"
FOOD_PREP_IDEAS_PATH = "food_prep_ideas.json"
BUTCHERING_IDEAS_PATH = "butchering_ideas.json"
CSA_SOURCES_PATH = "csa_sources.json"

# --- Utility Functions ---
def load_json(path, default):
    return load_json(path, default)

def save_json(path, obj):
    atomic_save_json(path, obj)

# --- Streamlit UI ---
def nutrition_ui():
    user_config = st.session_state.get('user_journal_config', {})
    toggles = user_config.get('toggles', {}) if user_config else {}
    if not toggles.get('nutrition', True):
        st.info("Nutrition & Recipe module is disabled in your configuration.")
        return
    st.title("Nutrition & Recipe Module")
    # Recipes
    st.header("Recipe Ideas")
    # --- Recipe Categories ---
    CATEGORIES = ["Stew", "Salad", "Mason Jar", "Soup", "Grain Bowl", "Other"]
    recipes = load_json(RECIPES_PATH, [])
    # Filter UI
    filter_cat = st.selectbox("Filter by Category", ["All"] + CATEGORIES, key="recipe_filter_cat")
    # Show grouped recipes with visual clarity
    grouped = {}
    for r in recipes:
        cat = r.get("category", "Other") if isinstance(r, dict) else "Other"
        grouped.setdefault(cat, []).append(r.get("name") if isinstance(r, dict) else r)
    for cat in (CATEGORIES if filter_cat == "All" else [filter_cat]):
        if cat in grouped:
            st.markdown(f"#### <span style='color:#1e88e5'>{cat}</span>", unsafe_allow_html=True)
            st.markdown("<ul style='margin-bottom:0.5em'>", unsafe_allow_html=True)
            for i, name in enumerate(grouped[cat]):
                st.markdown(f"<li style='font-size:1.1em'>{i+1}. {name}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
            # Highlight Mason Jar with sample recipe
            if cat == "Mason Jar" and grouped[cat]:
                st.info(f"**Sample Mason Jar Recipe:** {grouped[cat][0]}")
    # Quick Add for Mason Jar Stew
    st.markdown("<hr style='margin:1em 0;'>", unsafe_allow_html=True)
    st.markdown("### Quick Add: Mason Jar Stew 🫙")
    with st.form("quick_add_mason_jar"):
        mj_name = st.text_input("Recipe Name", value="Mason Jar Stew")
        mj_category = "Mason Jar"
        mj_submit = st.form_submit_button("Add Mason Jar Stew")
        if mj_submit and mj_name:
            recipes.append({"name": mj_name, "category": mj_category})
            save_json(RECIPES_PATH, recipes)
            st.success(f"Added: {mj_name} to Mason Jar recipes!")
            st.experimental_rerun()
    # Add new recipe (general)
    col1, col2 = st.columns([2,1])
    with col1:
        new_recipe = st.text_input("Add Recipe Idea", key="add_recipe_name")
    with col2:
        new_cat = st.selectbox("Category", CATEGORIES, key="add_recipe_cat")
    if st.button("Add Recipe") and new_recipe:
        recipes.append({"name": new_recipe, "category": new_cat})
        save_json(RECIPES_PATH, recipes)
        st.experimental_rerun()
    # Macro Cheat Sheet
    st.header("Macro Cheat Sheet")
    macro_cheat = load_json(MACRO_CHEATSHEET_PATH, {})
    if macro_cheat:
        for food, macro in macro_cheat.items():
            st.write(f"**{food}**: {macro}")
    new_food = st.text_input("Food Name for Macro Cheat Sheet")
    new_macro = st.text_input("Macros (e.g. 20g protein, 5g fat, 40g carb)")
    if st.button("Add Macro Cheat") and new_food and new_macro:
        macro_cheat[new_food] = new_macro
        save_json(MACRO_CHEATSHEET_PATH, macro_cheat)
        st.experimental_rerun()
    # Food Prep Ideas
    st.header("Mass Food Prep Ideas")
    prep_ideas = load_json(FOOD_PREP_IDEAS_PATH, [])
    for i, idea in enumerate(prep_ideas):
        st.write(f"{i+1}. {idea}")
    new_prep = st.text_input("Add Food Prep Idea")
    if st.button("Add Prep Idea") and new_prep:
        prep_ideas.append(new_prep)
        save_json(FOOD_PREP_IDEAS_PATH, prep_ideas)
        st.experimental_rerun()
    # Butchering Ideas
    st.header("Butchering & Sourcing Ideas")
    butchering_ideas = load_json(BUTCHERING_IDEAS_PATH, [])
    for i, idea in enumerate(butchering_ideas):
        st.write(f"{i+1}. {idea}")
    new_butcher = st.text_input("Add Butchering/Sourcing Idea")
    if st.button("Add Butchering Idea") and new_butcher:
        butchering_ideas.append(new_butcher)
        save_json(BUTCHERING_IDEAS_PATH, butchering_ideas)
        st.experimental_rerun()
    # CSA Sources
    st.header("CSA/Quality Meat Sources")
    csa_sources = load_json(CSA_SOURCES_PATH, [])
    for i, src in enumerate(csa_sources):
        st.write(f"{i+1}. {src}")
    new_csa = st.text_input("Add CSA/Meat Source")
    if st.button("Add CSA Source") and new_csa:
        csa_sources.append(new_csa)
        save_json(CSA_SOURCES_PATH, csa_sources)
        st.experimental_rerun()

if __name__ == "__main__":
    nutrition_ui()
