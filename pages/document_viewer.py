import streamlit as st
import re
from azure.cosmos import exceptions
from backend.modules.cosmos_db_connection import get_cosmos_client

container = get_cosmos_client("Customer Insights Platform", "Citations")

def get_doc_name_from_query():
    return st.query_params.get("doc_name")

def parse_conversation(conversation):
    lines = conversation.split("\n")
    conversation_pattern = re.compile(r"(\[\d+ minutes? \d+ seconds?\])?(\[.*?\])?\s*:\s*(.*)")
    
    parsed_data = [
        {
            'timestamp': timestamp.strip() if timestamp else None,
            'speaker': speaker.strip() if speaker else "Unknown",
            'message': message.strip()
        }
        for line in lines
        if (match := conversation_pattern.match(line)) and (timestamp := match.groups()[0]) and (speaker := match.groups()[1]) and (message := match.groups()[2])
    ]
    return parsed_data

def get_doc(doc_id):
    query = "SELECT * FROM Citations c WHERE c.doc_id = @doc_id" 
    parameters = [{"name": "@doc_id", "value": doc_id}]
    
    try:
        user_data = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True, partition_key=doc_id))
        return user_data[0] if user_data else None 
    except exceptions.CosmosResourceNotFoundError:
        return None

def display_document_viewer():
    doc_name = get_doc_name_from_query()
    
    if not doc_name:
        st.warning("No document selected.")
        return

    data = get_doc(doc_name)
    
    if not data:
        st.warning("⚠️ Document not found.")
        return

    st.title("📄 Document Viewer")
    document_content = data.get("Context")
    
    if document_content:
        st.subheader(f"📅 Date: {data.get('Date', 'N/A')}")
        st.subheader("🕒 Conversation Transcript")

        parsed_conversation = parse_conversation(document_content)
        for item in parsed_conversation:
            if item['timestamp']:
                st.markdown(f"**{item['timestamp']}**")
            st.markdown(f"**{item['speaker']}**: {item['message'].replace('$', '\\$')}")
            st.markdown("---")

display_document_viewer()
