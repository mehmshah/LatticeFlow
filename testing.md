# LatticeFlow Testing Checklist

## Macro Tracking: Label Scanner UI

### 1. UI Functionality
- [ ] The macro entry form appears in the “Label Scanner” tab under Macro Tracking.
- [ ] All fields are editable: Item Name, Serving Size, Protein (g), Carbs (g), Fat (g), Calories.
- [ ] The “Confirm Macros” button is present and clickable.

### 2. Data Entry & Logging
- [ ] Submitting the form with valid values adds the entry to the session log below.
- [ ] Multiple entries can be added and all appear in the log.
- [ ] The log displays the correct values for each entry.

### 3. Session Behavior
- [ ] The log resets when the page is refreshed (session-based, as expected).
- [ ] Submitting with blank or zero values is handled gracefully (no crash/UI error).

### 4. UX/Feedback
- [ ] Success message appears when an item is added.
- [ ] Table of confirmed macro entries is visible after at least one entry is submitted.

---

## AM Routine: ADHD Self-Awareness & Scripts Integration

### 1. Executive Function Audit
- [ ] Executive Function Audit table is displayed at the top of the ADHD Self-Awareness section.
- [ ] All audit domains, scores, priorities, and notes are visible and match the JSON.

### 2. Struggles & Strategies
- [ ] "What I Struggle With" and "Strategies & Tools Available" are shown as expanded details.
- [ ] All items are present and match the JSON file.

### 3. Design Principles
- [ ] "Key Design Principles" are shown as an expanded section (if present in JSON).
- [ ] All principles match the JSON file.

### 4. Scripts & Tools
- [ ] Each script/tool is shown as an expander with title, purpose, and steps/examples.
- [ ] All content matches the JSON file.
- [ ] No duplicate or missing scripts.

### 5. Upcoming Tools
- [ ] "Upcoming Tools" are shown in a collapsible expander (if present in JSON).
- [ ] All ideas/prototypes match the JSON file.

### 6. Navigation & UX
- [ ] "Next" and "Back" buttons move between AM routine steps correctly.
- [ ] No extra prompts, journaling, or checkboxes appear in the ADHD section.
- [ ] All ADHD sections are expanded by default for quick review.
- [ ] Editing the JSON and reloading the page updates all content accordingly.

---

## Future Testing (For OCR/Image Upload Feature)
- [ ] Image upload control appears and accepts food label images.
- [ ] OCR text extraction is shown to the user for review/copy.
- [ ] User can copy extracted text into macro fields and confirm as above.

---

*Update this checklist as new features are added or requirements change.*
