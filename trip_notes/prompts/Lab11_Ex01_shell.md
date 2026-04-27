Read src/models.py, src/storage.py, and src/ai_assistant.py first.

Create src/app.py — a Streamlit web app for Trip Notes AI.

---

## Layout

```
┌──────────────────────┬────────────────────────────────────────┐
│  ✈️ Trip Notes AI    │  💬 Chat  │  🔍 Search  │  🤖 Agent   │
│  ────────────────    │                                        │
│  📍 Current trip     │                                        │
│  [ Tokyo        ▼ ]  │     ℹ️  Coming soon — Exercise 2      │
│                      │         (placeholder for each tab)     │
│  📋 Notes (3)  [ ▼ ] │                                        │
│   • Great ramen...   │                                        │
│   • Train tip...     │                                        │
│                      │                                        │
│  [ Generate Briefing]│                                        │
└──────────────────────┴────────────────────────────────────────┘
```

---

## Behavior requirements

**Page setup:**
- Page title: "Trip Notes AI", page icon: ✈️, layout: wide
- `st.set_page_config()` must be the first Streamlit call in the file

**Session state (initialize once, before sidebar):**
- `"trips"` → result of `load_trips()`
- `"chat_history"` → empty list
- `"search_history"` → empty list
- `"agent_history"` → empty list

**Sidebar:**
- Title: "✈️ Trip Notes AI"
- Subtitle caption: "Powered by Atlas, your travel AI" (use `st.sidebar.caption()`)
- Selectbox labeled "📍 Current trip" — options are the names of all trips; if no trips, show `["(no trips yet)"]`
- If the selected trip has notes: show a collapsible expander labeled `📋 Notes (N)` listing each note with a bullet
- If the selected trip has no notes: show a small caption "No notes yet for this trip."
- "Generate Briefing" button:
  - If current trip has notes: call `ask()` with a briefing prompt that includes the trip name and its notes; display the result as markdown in the sidebar
  - If no notes: show a warning "Add some notes first."

**Main area:**
- Three tabs: `💬 Chat`, `🔍 Search`, `🤖 Agent`
- Each tab body: `st.info("Coming soon — Exercise 2")`, `st.info("Coming soon — Exercise 3")`, `st.info("Coming soon — Exercise 4")`

---

## Critical constraints

**Data access:** `load_trips()` returns a `TripCollection` object — it is NOT directly iterable. Call `.get_all()` to get the list of `Destination` objects. All loops and list comprehensions over trips must use `.get_all()`.

**sys.path fix:** Add these two lines at the very top of the file, before any imports:
```
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```
This is required so that `from src.x import ...` resolves correctly when running `streamlit run src/app.py` from the `trip_notes/` directory.

**Imports needed:** `streamlit`, `load_trips` from `src.storage`, `ask`, `TRAVEL_SYSTEM_PROMPT`, and `client` from `src.ai_assistant`. Do NOT import `rag_ask`, `run_agent`, or `ensure_index` yet.

**Run command** (from `trip_notes/`): `streamlit run src/app.py`

**Note on terminal warnings:** You may see a `ModuleNotFoundError: No module named 'torchvision'` message in the terminal when starting the app. This is a harmless warning from the `transformers` library (installed as part of Lab 09) and does not affect functionality. If the browser opens, the app is working correctly — ignore the warning.
