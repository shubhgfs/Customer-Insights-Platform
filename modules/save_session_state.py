import os
import uuid
import datetime
import streamlit as st
from azure.cosmos import exceptions
from modules.cosmos_db_connection import get_cosmos_client

container = get_cosmos_client("Marketing AI", "Chats")

def save_session_state():
    session_state_dict = dict(st.session_state)
    if 'authenticator' in session_state_dict:
        authenticator = session_state_dict['authenticator']
        del session_state_dict['authenticator']
        

    session_state_dict["timestamp"] = str(datetime.datetime.now())

    chat_id = st.session_state.get('selected_chat_id', str(uuid.uuid4()))
    session_state_dict["chat_id"] = chat_id

    document_id = st.session_state.get('selected_id', str(uuid.uuid4()))
    session_state_dict["id"] = document_id

    partition_key = chat_id

    try:
        container.read_item(document_id, partition_key=partition_key)
        container.delete_item(document_id, partition_key=partition_key)
    except exceptions.CosmosHttpResponseError as e:
        if e.status_code != 404:
            print(f"Error occurred while trying to delete document: {e.message}")

    try:
        container.upsert_item(session_state_dict, partition_key=partition_key)
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred: {e.message}")
        print("Document being uploaded:", session_state_dict)

    st.session_state['authenticator'] = authenticator
