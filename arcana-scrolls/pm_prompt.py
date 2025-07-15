def run_pm_prompt():
    print("\nLet’s pause for a full minute.\n")
    wait(60)
    print("Mantra: 'I choose commitment, integrity, control, and compassion for the best version of myself.'")

    input("Start with free-form reflection. Say 'Free reflection complete' when done.\n")
    reflection = capture_reflection()

    # Use GPT to generate proposed scores from reflection
    scores = gpt_score_metrics(reflection)
    confirmed_scores = confirm_scores(scores)

    # Relationship follow-ups if not mentioned
    for person in ["Gabby", "Cleo", "Parents", "Brother", "Friends"]:
        if person not in reflection:
            add_note = input(f"Would you like to expand on how things were with {person} today? → ")
            if add_note.strip():
                reflection += f"\n{person} note: {add_note}"

    tags = gpt_generate_tags(reflection)
    emotional_tags = gpt_emotional_scoring(reflection)

    # Macro summary
    macros = get_macro_summary()

    final_summary = gpt_summarize_day(reflection, confirmed_scores, macros)

    confirm = input("Ready to log full journal entry? (yes/no) → ")
    if confirm.lower() == "yes":
        logJournalEntry(reflection, confirmed_scores, tags, emotional_tags, macros, final_summary)
