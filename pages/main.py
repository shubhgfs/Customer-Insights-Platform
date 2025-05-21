import streamlit as st
from backend.modules.model_initializer import init_model, init_sql_agent, init_transcription_agent, init_team
from backend.modules.response_handler import get_team_response

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
    sql_agent = init_sql_agent(model)
    transcription_agent = init_transcription_agent(model)
    st.session_state.team = init_team(sql_agent, transcription_agent, model)

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

    with st.spinner("Thinking..."):
        response = get_team_response(st.session_state.team, prompt)
        assistant_msg = response.content

    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
    st.chat_message("assistant").write(assistant_msg)

# Sidebar options
st.sidebar.markdown("---")
if st.sidebar.button("Logout", type="primary"):
    if authenticator:
        authenticator.logout()
    st.session_state.clear()
    st.switch_page("login.py")
