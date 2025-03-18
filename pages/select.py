import streamlit as st
from azure.cosmos import exceptions
from modules.cosmos_db_connection import get_cosmos_client

container = get_cosmos_client("Customer Insights Platform", "Chats")
print('this is select page')
print(f'session state select.py: {st.session_state}')
print()
def get_chats(email):
    query = "SELECT * FROM Chats c WHERE c.user.email = @email"
    parameters = [{"name": "@email", "value": email}]
    try:
        return list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True)) or None
    except exceptions.CosmosResourceNotFoundError:
        return None

def set_chat_as_session_state(chat):
    st.session_state.update({
        'selected_id': chat['id'],
        'selected_chat_id': chat['chat_id'],
        'messages': chat['messages'],
        'selected_index': chat['selected_index']
    })

email = st.session_state['user']['email']
chats = get_chats(email)

st.markdown("<h2 style='text-align: center;'>Select a chat to continue</h2>", unsafe_allow_html=True)

if chats:
    st.write("### Your Previous Chats")
    col1, col2 = st.columns([3, 1])

    with col1:
        for chat in chats:
            chat_name = f'{chat["selected_index"]} - {chat["timestamp"]}'
            if st.button(chat_name, key=chat["chat_id"]):
                set_chat_as_session_state(chat)
                st.switch_page("pages/main.py")

    with col2:
        st.write("### Start a New Chat")
        if st.button("New Chat"):
            user = st.session_state['user']
            authentication_status = st.session_state['authentication_status']
            authenticator = st.session_state['authenticator']
            st.session_state.clear()
            st.session_state.update({'user': user, 'authentication_status': authentication_status, 'authenticator': authenticator})
            st.switch_page("pages/main.py")

if not chats:
    st.write("No chats found for this user. Start a new one!")
    if st.button("New Chat"):
        user = st.session_state['user']
        authentication_status = st.session_state['authentication_status']
        authenticator = st.session_state['authenticator']
        st.session_state.clear()
        st.session_state.update({'user': user, 'authentication_status': authentication_status, 'authenticator': authenticator})
        st.switch_page("pages/main.py")
