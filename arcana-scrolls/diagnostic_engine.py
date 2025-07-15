# runJournalDiagnostics
# This should be triggered after journaling is completed, but before /log-journal
# It inspects GPT behavior and output consistency across categories and halts if any logic failed.

def run_journal_diagnostics(journal_log, recent_logs, instruction_set):
    issues = []

    # 1. Trend Reference Check
    if not journal_log.get("trend_reference"):
        issues.append("Trend data not pulled or referenced.")

    # 2. Reflection Depth Check
    for section in journal_log.get("reflection_sections", []):
        if len(section.get("text", "").split()) < 12 and not section.get("deepening_prompt_issued"):
            issues.append(f"Section '{section['id']}' may need deepening.")

    # 3. Relationship Follow-Ups
    if journal_log.get("type") == "PM":
        for person in ["Gabby", "Cleo", "Parents", "Friends"]:
            if not journal_log.get("relationships", {}).get(person):
                issues.append(f"No reflection on {person}. Prompt may be missing.")

    # 4. Score Completeness
    for group, metrics in instruction_set["metric_groups"].items():
        for metric in metrics:
            if metric not in journal_log.get("scores", {}):
                issues.append(f"Missing score: {metric}")

    # 5. Emotion Tagging + Theme Tags
    if not journal_log.get("emotional_tags"):
        issues.append("No emotional tags detected.")
    if not journal_log.get("tags"):
        issues.append("No semantic tags applied.")

    # 6. Structure Check
    required_fields = ["free_reflection", "scores", "tags", "summary"]
    for f in required_fields:
        if f not in journal_log:
            issues.append(f"Missing required log section: {f}")

    # 7. AM Purpose Check
    if journal_log.get("type") == "AM":
        if not journal_log.get("purpose_confirmed"):
            issues.append("Morning purpose not reflected.")

    return issues
