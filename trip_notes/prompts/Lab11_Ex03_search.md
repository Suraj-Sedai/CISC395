Read src/app.py first.

Replace the `st.info("Coming soon — Exercise 3")` placeholder inside the Search tab with a RAG search interface. Do not modify the sidebar, tab1, or tab3.

Also add `ensure_index()` call and required imports.

---

## Layout

```
💬 Chat  │  🔍 Search  │  🤖 Agent

Search My Guides
Answers grounded in your guides/ documents.

┌──────────────────────────────────────────────┐
│  👤  What should I know about visiting       │
│      Tokyo?                                  │
│                                              │
│  🤖  Based on your guides, Tokyo is best     │
│      visited in spring or autumn...          │
└──────────────────────────────────────────────┘

[ Search your guides...                   ↵ ]   ← key="search_input"

[ Clear search ]
```

---

## Behavior requirements

- Add `from src.ai_assistant import rag_ask` and `from src.rag import ensure_index` to the imports at the top of app.py (if not already present)
- Call `ensure_index()` once at module level — place it after the session state initialization block and before the sidebar code. This builds or loads the RAG index when the app starts, so it is ready before any tab renders.
- Display all messages in `st.session_state["search_history"]` using `st.chat_message`
- Accept new input via `st.chat_input` with `key="search_input"`
- When the user submits:
  1. Append the user message to `"search_history"`
  2. Call `rag_ask(search_input)` with a spinner showing "Searching guides..."
  3. Display the response immediately
  4. Append the assistant response to `"search_history"`
- "Clear search" button: clears `st.session_state["search_history"]` and reruns; use `key="clear_search"`

---

## Critical constraints

- `ensure_index()` must be called at module level — NOT inside the tab block. If called inside the tab, it reruns on every user interaction.
- `st.chat_input` in this tab requires `key="search_input"` because tab1 already uses an unnamed `st.chat_input`; Streamlit will raise a `DuplicateWidgetID` error without it
- `st.session_state["search_history"]` is a separate list from `"chat_history"` — clearing one tab must not affect the other
- Do not change the sidebar, tab1, or tab3 code
