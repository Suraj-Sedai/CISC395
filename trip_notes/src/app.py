import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from src.ai_assistant import TRAVEL_SYSTEM_PROMPT, ask, client, MODEL, rag_ask
from src.storage import load_trips
from src.rag import ensure_index


st.set_page_config(page_title="Trip Notes AI", page_icon="✈️", layout="wide")


if "trips" not in st.session_state:
    st.session_state["trips"] = load_trips()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "search_history" not in st.session_state:
    st.session_state["search_history"] = []

if "agent_history" not in st.session_state:
    st.session_state["agent_history"] = []


ensure_index()


trips = st.session_state["trips"]
trip_list = trips.get_all()
trip_names = [trip.name for trip in trip_list]

st.sidebar.title("✈️ Trip Notes AI")
st.sidebar.caption("Powered by Atlas, your travel AI")

selected_name = st.sidebar.selectbox(
    "📍 Current trip",
    trip_names if trip_names else ["(no trips yet)"],
)

current_trip = next(
    (trip for trip in trip_list if trip.name == selected_name),
    None,
)

if current_trip is not None:
    if current_trip.notes:
        with st.sidebar.expander(f"📋 Notes ({len(current_trip.notes)})"):
            for note in current_trip.notes:
                st.markdown(f"- {note}")
    else:
        st.sidebar.caption("No notes yet for this trip.")
else:
    st.sidebar.caption("No notes yet for this trip.")

if st.sidebar.button("Generate Briefing"):
    if current_trip is not None and current_trip.notes:
        notes_text = "\n".join(f"- {note}" for note in current_trip.notes)
        briefing_prompt = (
            f"Create a concise travel briefing for {current_trip.name} using "
            f"these trip notes:\n\n{notes_text}"
        )
        briefing = ask(briefing_prompt, system_prompt=TRAVEL_SYSTEM_PROMPT)
        if briefing:
            st.sidebar.markdown(briefing)
        else:
            st.sidebar.warning("Unable to generate a briefing right now.")
    else:
        st.sidebar.warning("Add some notes first.")

chat_tab, search_tab, agent_tab = st.tabs(["💬 Chat", "🔍 Search", "🤖 Agent"])

with chat_tab:
    st.subheader("Atlas — Your Travel AI")
    st.caption("Ask me anything about travel.")

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Ask Atlas anything..."):
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        MAX_TURNS = 8
        messages = [{"role": "system", "content": TRAVEL_SYSTEM_PROMPT}]
        messages.extend(st.session_state["chat_history"][:-1][-(MAX_TURNS * 2) :])
        messages.append({"role": "user", "content": user_input})

        with st.spinner("Atlas is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                )
                assistant_response = response.choices[0].message.content
                if assistant_response:
                    with st.chat_message("assistant"):
                        st.markdown(assistant_response)
                    st.session_state["chat_history"].append(
                        {"role": "assistant", "content": assistant_response}
                    )
                else:
                    st.error("Atlas couldn't think of a response.")
            except Exception as e:
                st.error(f"Error communicating with Atlas: {e}")

    if st.button("Clear chat", key="clear_chat"):
        st.session_state["chat_history"] = []
        st.rerun()

with search_tab:
    st.subheader("Search My Guides")
    st.caption("Answers grounded in your guides/ documents.")

    for message in st.session_state["search_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if search_input := st.chat_input("Search your guides...", key="search_input"):
        st.session_state["search_history"].append({"role": "user", "content": search_input})
        with st.chat_message("user"):
            st.markdown(search_input)

        with st.spinner("Searching guides..."):
            response = rag_ask(search_input)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state["search_history"].append(
                {"role": "assistant", "content": response}
            )

    if st.button("Clear search", key="clear_search"):
        st.session_state["search_history"] = []
        st.rerun()

with agent_tab:
    st.info("Coming soon — Exercise 4")
