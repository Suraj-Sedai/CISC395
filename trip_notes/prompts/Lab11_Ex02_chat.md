Read src/app.py and src/ai_assistant.py first.

Replace the `st.info("Coming soon — Exercise 2")` placeholder inside the Chat tab with a working chat interface. Do not modify the sidebar, tab2, or tab3.

---

## Layout

```
💬 Chat  │  🔍 Search  │  🤖 Agent

Atlas — Your Travel AI
Ask me anything about travel.

┌──────────────────────────────────────────────┐  ↑
│  👤  What are good things to pack for a      │  │
│      rainy-season trip to Southeast Asia?    │  │  chat history
│                                              │  │  (scrollable,
│  🤖  Great question! For rainy season...     │  │   rendered top
│                                              │  │   to bottom)
│  👤  Which of those also work for cold       │  │
│      mountain trips?                         │  │
│                                              │  │
│  🤖  For colder mountain conditions...       │  ↓
└──────────────────────────────────────────────┘

[ Ask Atlas anything...                   ↵ ]   ← st.chat_input pinned at bottom

[ Clear chat ]
```

**Render order matters:** history first (top), then `st.chat_input` (bottom). This is how Streamlit pins the input correctly.

---

## Behavior requirements

**Subheader and caption:**
- `st.subheader("Atlas — Your Travel AI")`
- `st.caption("Ask me anything about travel.")`

**Chat history display:**
- Render all messages in `st.session_state["chat_history"]` using `st.chat_message` with each message's `"role"` field before the input widget

**Multi-turn memory (important):**
- When sending to the API, do NOT call `ask()` — build the messages list manually using `client` directly
- Keep the last `MAX_TURNS = 8` turns (16 messages: 8 user + 8 assistant) from `"chat_history"` to avoid context overflow
- Message structure to send:
  ```
  [system: TRAVEL_SYSTEM_PROMPT]
  + last MAX_TURNS * 2 messages from chat_history
  + current user message
  ```
- Use `client.chat.completions.create(model=MODEL, messages=messages)` and extract `.choices[0].message.content`
- Wrap the API call in a spinner showing "Atlas is thinking..."

**On new user input:**
1. Append `{"role": "user", "content": user_input}` to `"chat_history"`
2. Call the API with the trimmed history + current message
3. Display the assistant response with `st.chat_message("assistant")`
4. Append `{"role": "assistant", "content": response}` to `"chat_history"`

**Clear chat button:**
- Label: "Clear chat", `key="clear_chat"`
- Clears `st.session_state["chat_history"]` and calls `st.rerun()`

---

## Critical constraints

- Import `client` and `MODEL` from `src.ai_assistant` (already imported in Ex01 — do not duplicate)
- `TRAVEL_SYSTEM_PROMPT` already defines Atlas's persona — do not redefine a system prompt
- `st.chat_input` in tab1: use default key (no `key=` parameter); tabs 2 and 3 will need explicit keys
- History slice: `chat_history[-(MAX_TURNS * 2):]` — always trim before sending, never truncate the stored history
- Do not change the sidebar, tab2, or tab3 code
