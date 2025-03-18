import os
import openai
import dotenv
import httpx
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import warnings
import urllib
from azure.cosmos import CosmosClient, exceptions
from modules.process_citations import process_citations
from modules.save_session_state import save_session_state
from modules.select_default_index import get_indexes, select_index
from modules.select_default_agent import get_agents, select_agent
from modules.cosmos_db_connection import get_cosmos_client

warnings.filterwarnings("ignore", message="{warning_message}")
dotenv.load_dotenv()

container_index = get_cosmos_client("Marketing AI", "Indexes")
container_agent = get_cosmos_client("Marketing AI", "Agents")

index_names = get_indexes(container_index)
selected_index = st.session_state.get("selected_index")
default_category, default_subcategory, default_status = select_index(index_names, selected_index)

agent_data = get_agents(container_agent)
selected_agent = st.session_state.get("selected_agent")
default_agent, default_system, default_temperature = select_agent(agent_data, selected_agent)

authenticator = st.session_state.get('authenticator')

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
    st.rerun()

elif st.session_state['authentication_status']:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY_AQMAGENTICOS")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION_AQMAGENTICOS")

    http_client = httpx.Client(verify=False)

    client = openai.AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        http_client=http_client
    )

    st.title("💬 Marketing Chatbot")

    st.sidebar.title("Select Chatbot")
    categories = index_names["Brand"].unique()
    selected_category = st.sidebar.selectbox("Brand", categories, index=list(categories).index(default_category) if default_category in categories else 0)

    filtered_subcategories = index_names[index_names["Brand"] == selected_category]['Product'].unique()
    selected_subcategory = st.sidebar.selectbox("Product", filtered_subcategories, index=list(filtered_subcategories).index(default_subcategory) if default_subcategory in filtered_subcategories else 0)

    filtered_statuses = index_names[(index_names["Brand"] == selected_category) & (index_names["Product"] == selected_subcategory)]['Sale Status'].unique()
    selected_status = st.sidebar.selectbox("Sale Status", filtered_statuses, index=list(filtered_statuses).index(default_status) if default_status in filtered_statuses else 0)

    selected_index_row = index_names[
        (index_names["Brand"] == selected_category) & 
        (index_names["Product"] == selected_subcategory) & 
        (index_names["Sale Status"] == selected_status)]

    if not selected_index_row.empty:
        selected_index = selected_index_row.iloc[0]["Index Name"]

    if 'selected_index' not in st.session_state:
        st.session_state["selected_index"] = selected_index

    if st.sidebar.button("Confirm Chatbot"):
        if "messages" in st.session_state and len(st.session_state["messages"]) > 1:
            save_session_state()
        del st.session_state["messages"]
        st.session_state["selected_index"] = selected_index
        st.rerun()

    st.sidebar.markdown("---")

    st.sidebar.title("Select Agent")
    agents = agent_data['Agent Name'].unique()
    selected_agent = st.sidebar.selectbox("Agent", agents, index=list(agents).index(default_agent) if default_agent else 0)
    system = agent_data[agent_data['Agent Name'] == selected_agent]['System'].iloc[0]
    temperature = agent_data[agent_data['Agent Name'] == selected_agent]['Temperature'].iloc[0]

    if 'selected_agent' not in st.session_state:
        st.session_state["selected_agent"] = selected_agent
    if 'system' not in st.session_state:
        st.session_state["system"] = system
    if 'temperature' not in st.session_state:
        st.session_state["temperature"] = temperature

    if st.sidebar.button("Confirm Agent"):
        st.session_state["selected_agent"] = selected_agent
        st.session_state["system"] = system
        st.session_state["temperature"] = temperature
        st.rerun()

    st.sidebar.markdown("---")

    product_name = f"{selected_category} {selected_subcategory}"
    encoded_product_name = urllib.parse.quote(product_name)

    st.sidebar.markdown("""
        <style>
        .help-button {
            display: inline-block;
            background-color: #F0F2F6;
            color: black;
            padding: 10px 20px;
            border-radius: 5px;
            border: 2px solid #ccc;
            text-decoration: none;
            font-weight: bold;
            text-align: center;
        }
        .help-button:hover {
            background-color: #ADD8E6;
        }
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.markdown(f'<a href="help?product_name={encoded_product_name}" class="help-button">Need help?</a>', unsafe_allow_html=True)
    st.sidebar.markdown("---")

    if st.sidebar.button("Go to Select Page"):
        save_session_state()
        st.switch_page("pages/select.py")

    st.sidebar.markdown("---")

    if st.sidebar.button("Logout", type="primary"):
        save_session_state()
        authenticator.logout()
        st.switch_page('login.py')


    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": f"How can I help you with getting insights about customer interactions for {selected_category} {selected_subcategory} {selected_status}?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask something about customer interactions..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        messages = [{"role": "system", "content": "You are a marketing chatbot using data from call recordings between customers and sales agents."}] + st.session_state.messages if 'chat_id' not in st.session_state else st.session_state.messages

        completion = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=temperature,
            extra_body={
                "data_sources": [{
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],
                        "index_name": st.session_state['selected_index'],
                        "authentication": {
                            "type": "api_key",
                            "key": os.environ["AZURE_AI_SEARCH_API_KEY"],
                        },
                        "role_information": f'{system}'
                    }
                }],
            }
        )

        msg = process_citations(completion)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.switch_page('login.py')
    st.warning('Please enter your username and password')
