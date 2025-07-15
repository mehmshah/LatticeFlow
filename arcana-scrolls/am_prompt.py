def run_am_prompt():
    print("\nLet’s pause for a full minute.\n")
    wait(60)
    print("Mantra: 'I choose commitment, integrity, control, and compassion for the best version of myself.'")

    ready = input("Are you ready to proceed? (yes to continue) → ")
    if ready.lower() != "yes": return

    print("Sleep Scoring (1–10): 7 hours = 10/10. Halve the score for 3.5 hours. Round based on quality as well.")
    sleep_hours = input("How many hours did you sleep last night? → ")
    print("Sleep Quality (1–10): 1 = very poor (<4h), 5 = light/interrupted, 10 = rested/uninterrupted")
    sleep_quality = input("Based on the above, how would you score your sleep quality? → ")
    print("Energy Level (1–10): 1 = depleted, 5 = functional but tired, 10 = energized and clear")
    energy_score = input("What is your current energy level? → ")

    adhd_plan = input("What is your ADHD focus for today? → ")
    strategy = input("What strategy will support this? → ")
    success = input("What would make today feel like a success? → ")

    intentions = {
        "Gabby": input("How do you want to show up for Gabby today? → "),
        "Cleo": input("What is your intention for Cleo today? → "),
        "Parents/Brother": input("Any follow-up needed for your parents or brother today? → "),
        "Friends": input("How might you reach out to friends today? → ")
    }

    confirm = input("Ready to log morning reflection? (yes/no) → ")
    if confirm.lower() == "yes":
        save_am_log(sleep_hours, sleep_quality, energy_score, adhd_plan, strategy, success, intentions)
