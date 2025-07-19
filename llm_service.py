"""
llm_service.py
Centralized module for all LLM (ChatGPT/OpenAI) calls for LatticeFlow.
Uses a dummy API key for scaffolding. Replace with your real key in production.
"""
import os
import openai

def get_openai_api_key():
    # 1. Streamlit session_state (runtime entry)
    try:
        import streamlit as st
        if hasattr(st, 'session_state') and 'openai_api_key' in st.session_state:
            return st.session_state['openai_api_key']
    except ImportError:
        pass
    # 2. Environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    # 3. Streamlit secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except ImportError:
        pass
    # 4. Dummy fallback with warning
    print("[llm_service.py] WARNING: No OpenAI API key found in session, env, or Streamlit secrets. Using dummy key. LLM features will not work.")
    return "sk-dummy-key"

openai.api_key = get_openai_api_key()

# ---- Prompt templates ----
PROMPTS = {
    "onboarding_extract": lambda user_text: f"""
Given the following user description, extract their main life domains/focuses, influential entities (people, organizations, etc), suggested metrics (archetype or custom), and which of these features they want enabled: calendar, weather, ADHD toolkit, mantra, export, style (dark/light).

Return a JSON object with the following format:
{{
  \"domains\": [\"domain1\", \"domain2\"],
  \"entities\": [\"entity1\", \"entity2\"],
  \"metrics\": [\"metric1\", \"metric2\"],
  \"toggles\": {{\"calendar\": true, \"weather\": false, \"adhd\": true, \"mantra\": false, \"export\": true, \"style\": \"Light\"}}
}}

User description:
{user_text}
Respond ONLY with the JSON object, no explanations or extra text.
""",

    "meal_suggestion": lambda ingredients, meal_type: f"""
Suggest 3 healthy {meal_type} recipes I can make with the following ingredients:
{', '.join(ingredients)}
Respond in markdown with a bulleted list. Use standard US nutrition guidelines for your suggestions.
""",
    "macro_analysis": lambda food_desc: f"""
Estimate the macros (protein, carbs, fat, calories) for the following meal:
"{food_desc}"
Use standard US nutrition guidelines. Respond as a table.
""",
    "pm_metric_scoring": lambda reflection, relationships, metrics: f"""
Given the following free reflection and relationship log, score these metrics from 1-10 and explain your reasoning for each:
Reflection: {reflection}
Relationships: {relationships}
Metrics: {', '.join(metrics)}
Respond as JSON: {{metric: score, explanation}}
""",
    "trend_analysis": lambda logs: f"""
Analyze the following journal logs for trends, recurring themes, and suggest one area to focus on this week:
{chr(10).join(logs)}
Respond with a summary paragraph.
""",
    "workout_feedback": lambda workout_log: f"""
Based on the following workout log and RPEs, suggest how I should adjust my weights and reps for each exercise next week:
{workout_log}
Respond as a table: Exercise | Last Week | RPE | Suggested Change | Reasoning
""",

    "journal_surface_check": lambda entry: f"""
Here is a journal entry:
{entry}
1. Is this entry surface-level or lacking depth? (yes/no)
2. If yes, suggest a follow-up question or prompt that would help the user reflect more deeply.
3. If no, reply with "No further prompt needed."
Respond as JSON: {{"surface_level": "yes/no", "prompt": "string"}}
""",

    "tagging": lambda entry: f"""
Read this journal entry and return a list of emotions and themes present. Respond as JSON: {{"emotions": [], "themes": []}}
Entry:
{entry}
"""
}

# ---- LLM call helpers ----
def chat_with_llm(messages, system_prompt=None, model="gpt-4o", max_tokens=512, temperature=0.7):
    """
    Unified LLM chat interface for all modules.
    Args:
        messages: List of dicts [{"role": "user"/"assistant", "content": str}]
        system_prompt: Optional string for system context.
        model: OpenAI model name.
        max_tokens: Max tokens for response.
        temperature: Sampling temperature.
    Returns:
        Assistant reply string, or error message.
    """
    try:
        chat_msgs = []
        if system_prompt:
            chat_msgs.append({"role": "system", "content": system_prompt})
        chat_msgs.extend(messages)
        response = openai.ChatCompletion.create(
            model=model,
            messages=chat_msgs,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[llm_service.py] LLM error: {e}")
        return "[Sorry, there was a problem contacting the LLM. Please try again later.]"

def call_openai(prompt, model="gpt-4o", max_tokens=512, temperature=0.7):
    """
    Legacy single-prompt interface. Use chat_with_llm for new code.
    """
    return chat_with_llm([{"role": "user", "content": prompt}], model=model, max_tokens=max_tokens, temperature=temperature)

# ---- Main API ----
def extract_onboarding_config(user_text):
    prompt = PROMPTS["onboarding_extract"](user_text)
    raw = call_openai(prompt, max_tokens=512, temperature=0.2)
    import json
    try:
        parsed = json.loads(raw)
        return parsed
    except Exception:
        # Try to extract JSON from text if LLM wraps output
        import re
        match = re.search(r'\{[\s\S]*\}', raw)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        raise ValueError(f"Could not parse onboarding config from LLM output: {raw}")

def get_meal_suggestions(ingredients, meal_type="dinner"):
    prompt = PROMPTS["meal_suggestion"](ingredients, meal_type)
    return call_openai(prompt)

def analyze_macros(food_desc):
    prompt = PROMPTS["macro_analysis"](food_desc)
    return call_openai(prompt)

def auto_score_pm_metrics(reflection, relationships, metrics):
    prompt = PROMPTS["pm_metric_scoring"](reflection, relationships, metrics)
    return call_openai(prompt)

def analyze_trends(logs):
    prompt = PROMPTS["trend_analysis"](logs)
    return call_openai(prompt)

def get_workout_feedback(workout_log):
    prompt = PROMPTS["workout_feedback"](workout_log)
    return call_openai(prompt)

def check_journal_surface(entry):
    prompt = PROMPTS["journal_surface_check"](entry)
    return call_openai(prompt)

def tag_journal_entry(entry):
    prompt = PROMPTS["tagging"](entry)
    return call_openai(prompt)

# ---- TODO: Add caching, error handling, and Assistant API support for trend analysis ----
