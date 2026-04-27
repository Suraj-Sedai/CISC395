Read src/app.py and src/tools.py first.

Replace the `st.info("Coming soon — Exercise 4")` placeholder inside the Agent tab with a ReAct agent interface. Do not modify the sidebar, tab1, or tab2.

---

## Layout

```
💬 Chat  │  🔍 Search  │  🤖 Agent

AI Travel Agent
The agent uses tools: budget calculation, live weather, and guide search.

Your question:
┌──────────────────────────────────────────────────────┐
│  e.g. I have $1200 for 8 days in Tokyo. Check the   │
│  weather and break down my budget.                   │
│                                                      │  ← st.text_area (resizable)
└──────────────────────────────────────────────────────┘

[ Ask the Agent ]

──────────────────────────────────────────────────────
Agent answer displayed here as markdown
──────────────────────────────────────────────────────

▶ Tools available to this agent
   • budget_breakdown
   • get_weather
   • search_guides_tool

──────────────────────────────────────────────────────
Previous queries this session:
  ▶ Q: I have $900 for 6 days in Tokyo...
       [answer hidden in expander]
```

---

## Behavior requirements

- Add `from src.tools import run_agent, TOOL_DEFINITIONS` to the imports (if not already present)
- Use `st.text_area` (not `st.chat_input`) for the question input — agent questions are longer and benefit from a resizable box; give it a descriptive placeholder
- "Ask the Agent" button: only runs if the text area is not empty
  - Show a spinner with "Agent is working..." while `run_agent(question)` executes
  - Display the returned answer as markdown
  - Show a collapsible expander "Tools available to this agent" listing each tool name from `TOOL_DEFINITIONS`
  - Append `{"question": question, "answer": answer}` to `st.session_state["agent_history"]`
- Below the current result, show all previous queries from `"agent_history"` in reverse order (newest first), each as a collapsible expander with the question (truncated to ~60 chars) as the label and the answer as the body

---

## Critical constraints

- `run_agent()` prints `[Tool call]` and `[Tool result]` lines to the terminal where `streamlit run` is running — these do NOT appear in the browser. Do not try to capture or display them in the UI.
- Tool names come from `TOOL_DEFINITIONS` — read each entry's `"function"` → `"name"` field
- `st.session_state["agent_history"]` stores dicts with `"question"` and `"answer"` keys — use these exact key names
- Do not change the sidebar, tab1, or tab2 code
