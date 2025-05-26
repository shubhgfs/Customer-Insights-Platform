import streamlit as st
import json
from streamlit_lottie import st_lottie
from backend.modules.model_initializer import (
    init_model,
    init_sql_agent,
    init_transcription_agent,
    init_team
)
from backend.modules.response_handler import get_team_response
from backend.modules.save_session_state import save_session_state
import time
import random
import uuid

# Class A: Initial Thinking Phase
initial_thinking_messages = [
    "Thinking...",
    "Processing your request...",
    "Reasoning through your input...",
    "Exploring possibilities...",
    "Analyzing context...",
    "Evaluating relevant information...",
    "Scanning for patterns...",
    "Absorbing your query...",
    "Working through the logic...",
    "Reflecting on your question..."
]

# Class B: Finalizing Response Phase
finalizing_response_messages = [
    "Piecing together the final response...",
    "Composing your answer...",
    "Structuring the insight...",
    "Finalizing thoughts...",
    "Refining the response...",
    "Formatting your answer...",
    "Bringing everything together...",
    "Wrapping it up...",
    "Just a moment more...",
    "Almost ready..."
]

first_name = st.session_state['user']['name'].split()[0] if 'user' in st.session_state else "User"

# Load Lottie animation
@st.cache_data
def load_lottie_animation(path):
    with open(path, "r") as f:
        return json.load(f)

animation = load_lottie_animation("backend/json files/animation.json")

# Optional: Load authenticator from session state
authenticator = st.session_state.get("authenticator")

# Authentication check
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
    st.rerun()

elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
    st.stop()

elif st.session_state["authentication_status"] is None:
    st.switch_page("login.py")
    st.warning("Please enter your username and password")
    st.stop()

# Ensure a persistent chat ID for the session
if "chat_id" not in st.session_state:
    st.session_state["chat_id"] = str(uuid.uuid4())

# Ensure a persistent document ID for the session
if "document_id" not in st.session_state:
    st.session_state["document_id"] = str(uuid.uuid4())

# ---------- Main Chatbot App ----------
st.title("💬 Customer Insight Chatbot")

# Initialize backend (run once per session)
if "team" not in st.session_state:
    model = init_model()
    print("Model initialized")
    sql_agent = init_sql_agent(model)
    print("SQL agent initialized")
    transcription_agent = init_transcription_agent(model)
    print("Transcription agent initialized")
    st.session_state.team = init_team(sql_agent, transcription_agent, model)
    print("Customer Insight Team initialized and added to session state")

# Message history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": f"Hi {first_name}! How can I help you gain insights from customer interactions today?"
    }]

# Render message history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question to the team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with placeholder.container():
            starting_message = random.sample(initial_thinking_messages, k=2)
            ending_message = random.sample(finalizing_response_messages, k=2)
            st_lottie(animation, height=100, key="thinking", quality="high", width=100)
            msg_placeholder = st.empty()
            for msg in starting_message:
                msg_placeholder.markdown(f"**{msg}**")
                time.sleep(3)

        response = get_team_response(st.session_state.team, prompt)
        assistant_msg = response.get(
            "content",
            "Sorry, I couldn't find an answer to your question. Server is currently down."
        )

        msg_placeholder.empty()
        for msg in ending_message:
            msg_placeholder.markdown(f"**{msg}**")
            time.sleep(3)
            msg_placeholder.empty()
            
        placeholder.empty()
        st.write(assistant_msg)

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_msg,
        "ai_full_response": response,
    })
    save_session_state()

    # Subtle disclaimer below chat input
    st.badge("ℹ️ Trust AI, but verify!")

# ---------- Sidebar ----------

st.sidebar.title(f"Welcome, {st.session_state['user']['name']}! 👋")
st.sidebar.markdown("---")

# Create the "New Session" button in the sidebar with a unique key
if st.sidebar.button("New Session 🆕", help='Start a new session.'):
    if authenticator:
        save_session_state()
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("SQL Agent Disclaimer: The data in the SQL is from January 2022 till May 2025.")
st.sidebar.info("Transcription Agent Disclaimer: The data in the transcription is from October 2024 till March 2025.")
st.sidebar.warning("🤖 Trust AI, but verify!")

st.sidebar.markdown("---")

if st.sidebar.button("FAQ ❓", help='Frequently Asked Questions'):
    st.switch_page("pages/help.py")

st.sidebar.markdown("---")

if st.sidebar.button("Logout", type="primary"):
    if authenticator:
        save_session_state()
        authenticator.logout()
    st.session_state.clear()
    st.switch_page("login.py")
