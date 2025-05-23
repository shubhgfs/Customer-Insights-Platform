import streamlit as st
import json
from backend.modules.model_initializer import init_model, init_sql_agent, init_transcription_agent, init_team
from backend.modules.response_handler import get_team_response
from backend.modules.save_session_state import save_session_state
from streamlit_lottie import st_lottie

# Load Lottie animation
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
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! How can I help you gain insights from customer interactions today?"}
    ]

# Render message history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question to the team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Show thinking animation
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with placeholder.container():
            st_lottie(animation, height=100, key="thinking", quality="high", width=100)
            st.markdown("Thinking...")

        response = get_team_response(st.session_state.team, prompt)
        assistant_msg = response.content

        placeholder.empty()
        st.write(assistant_msg)  # Final response within same assistant block

    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

# Sidebar options
st.sidebar.markdown("---")
if st.sidebar.button("Logout", type="primary"):
    if authenticator:
        save_session_state()
        authenticator.logout()
    st.session_state.clear()
    st.switch_page("login.py")
