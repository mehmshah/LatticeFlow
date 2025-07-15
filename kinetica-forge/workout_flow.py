# Pre/Post Workout Scoring Frameworks
# Energy: 1 = depleted, 5 = functional but tired, 10 = fully energized
# Mood: 1 = anxious/irritable, 5 = neutral, 10 = positive/uplifted
# Recovery: 1 = sore/exhausted, 5 = okay, 10 = fully recovered

def prompt_score(label):
    print(f"{label} Scoring (1–10):")
    print("1 = depleted / low, 5 = neutral, 10 = energized / clear")
    return input(f"{label} → ")

def get_energy_mood_recovery(phase):
    print(f"\n🔄 {phase.title()}-Workout Scoring")
    energy = prompt_score("Energy")
    mood = prompt_score("Mood")
    recovery = prompt_score("Recovery")
    return {"energy": energy, "mood": mood, "recovery": recovery}

# Pre/Post Workout Scoring Frameworks
# Energy: 1 = depleted, 5 = functional but tired, 10 = fully energized
# Mood: 1 = anxious/irritable, 5 = neutral, 10 = positive/uplifted
# Recovery: 1 = sore/exhausted, 5 = okay, 10 = fully recovered

def run_workout_session():
    show_workout_day()
    pre_scores = get_energy_mood_recovery("pre")

    run_section("Warm-up Bike")
    run_section("Warm-up Exercises")

    for superset in load_today_supersets():
        run_superset(superset)

    run_section("Cool-down Stretches")
    post_scores = get_energy_mood_recovery("post")

    tags = gpt_generate_workout_tags()
    notes = input("Any notes you'd like to remember? → ")
    log_workout(pre_scores, post_scores, tags, notes)
