import streamlit as st
from backend.modules.model_initializer import init_model, init_sql_agent, init_transcription_agent, init_team
from backend.modules.response_handler import get_team_response

# Initialize once
model = init_model()
sql_agent = init_sql_agent(model)
transcription_agent = init_transcription_agent(model)
team = init_team(sql_agent, transcription_agent, model)

st.title("Customer Insight Chatbot")

query = st.text_input("Ask a question to the team:")
if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        response = get_team_response(team, query)
        st.markdown(response.content)
