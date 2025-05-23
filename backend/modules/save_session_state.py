import os
import uuid
import pytz
import datetime
import streamlit as st
from azure.cosmos import exceptions
from backend.modules.cosmos_db_connection import get_cosmos_client

container = get_cosmos_client("Customer Insights Platform", "Chats")

def get_sydney_time_now():
    sydney_tz = pytz.timezone("Australia/Sydney")
    sydney_time = datetime.datetime.now(sydney_tz).isoformat()
    return sydney_time

def save_session_state():
    session_state_dict = dict(st.session_state)
    # print('session_state_dict:', session_state_dict)
    
    session_state_dict.pop('team')

    if 'authenticator' in session_state_dict:
        authenticator = session_state_dict['authenticator']
        del session_state_dict['authenticator']
        

    session_state_dict["updated_at"] = str(get_sydney_time_now())

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
        print('Uploading document to Cosmos DB:', session_state_dict)
        container.upsert_item(session_state_dict, partition_key=partition_key)
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred: {e.message}")
        print("Document being uploaded:", session_state_dict)

    st.session_state['authenticator'] = authenticator
