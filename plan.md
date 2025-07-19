# LatticeFlow Planning

## Notes
- Implementation must strictly follow the canvas: module structure, file names, logic flows, and UI requirements.
- No improvisation or generalization beyond the canvas.
- Do not replace or template specific files: pm_prompt.py, runJournalDiagnostics, metric_groups.json.
- GPT API is used for scoring, tagging, and summaries; trend analysis will use Assistants later.
- All output must follow the Markdown and JSON schema described in the canvas.
- Never start a new plan.md file; always centralize notes and tasks here.
- The full system specification (canvas) has been received from the user.



## LatticeFlow Steps
### Implementation Plan
> All other internal modularization tasks for journaling are now **DONE** except for Calendar/Weather integration.

#### 🔴 Higher Complexity / Multi-step / Cross-cutting
- [x] System Architecture & Export: Move/refactor files and folders to match modular structure (e.g., all ADHD-related items to beemind, etc.)
- [x] Workout Tracker: Last Week's Performance Integration (progression system)
- [x] Workout Tracker: Decide on OCR/image upload flow or chatbot pipeline
- [x] Journaling & Diagnostics: UI final wiring for summaries and confirmation steps (modular session-state-driven diagnostics preview and confirmation step added to **both** AM/PM flows, mobile-friendly, LLM-powered, explicit user confirmation before save; **AM journal modular implementation and diagnostics UI is now complete and matches project canvas**) 
- [x] Journaling & Diagnostics: UI integration for diagnostics preview (Streamlit diagnostics page updated, per-entry LLM-powered diagnostics and summary preview wired in, mobile-optimized)
- [x] Journaling & Diagnostics: Complete emotion tagging and semantic tags extraction (LLM-powered tagging and emotion extraction now active in both AM/PM flows, not stubbed)
- [ ] PM Journal Enhancements: Relationship Follow-ups Section (**deferred to onboarding-driven logic, not implemented now**)
- [ ] PM Journal Enhancements: Auto-scoring from Reflections (free reflection + relationship follow-ups)
- [x] Macro Tracking: ChatGPT-style conversational interface (multi-turn, persistent context, natural chat UI)
- [x] Extend ChatGPT-style conversational UI pattern to Diagnostics module (journaling review, trends, and feedback)
- [x] Extend ChatGPT-style conversational UI pattern to Meal Planning and other LLM-powered modules
- [x] System Architecture & Export: GPT Integration for reflection analysis and auto-scoring
    - All LLM-powered scoring, tagging, and trend analysis is now centralized, robust, and fully tested.
- [x] System Architecture & Export: Data Persistence (proper database or file-based storage system)
    - Robust atomic JSON persistence with backups is now in place across all core modules.

---

## Milestone: Gold Standard Routine Builder Architecture (2025-07-18)

- Onboarding refactored to support the gold standard: users now build their AM/PM/workout routines as editable arrays of typed components.
- Supported types: prompt, metric, checklist, avoidance, intention, reflection, exercise, timer, resource.
- Users can reorder, edit, change type, and set privacy for each routine step before saving.
- Architecture is ready for LLM-powered parsing of freeform input into structured routines.
- Main app will render routines dynamically from this config, enabling deep personalization and extensibility (journaling, wellness, diagnostics, workout modules, etc.).
- Privacy handled via conversational prompts; all onboarding questions are mandatory.
- Periodic (6-month) check-in planned to prompt users to review/update their routines.

### Internal Checklist
- [x] Data model refactor: routines as arrays of typed components
- [x] Editable draft routine review UI
- [ ] LLM integration for parsing and suggestion
- [ ] Dynamic rendering of routines in AM/PM/workout modules
- [ ] Privacy controls (private steps hidden from analytics/prompts)
- [ ] Periodic onboarding check-in logic

<!-- Add new milestones and architecture changes here -->
