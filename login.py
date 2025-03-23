import os
import dotenv
import bcrypt
import streamlit as st
import streamlit_authenticator as stauth
from azure.cosmos import exceptions
from modules.cosmos_db_connection import get_cosmos_client
import warnings
warnings.filterwarnings("ignore")

dotenv.load_dotenv()

container = get_cosmos_client("Customer Insights Platform", "Users")

query = "SELECT * FROM Users u WHERE u.email = 'cookie-cip@gfs.com.au'"
cookie_data = list(container.query_items(query=query, enable_cross_partition_query=True))[0]

query = "SELECT * FROM Users u WHERE u.email <> 'cookie-cip@gfs.com.au'"
user_data = list(container.query_items(query=query, enable_cross_partition_query=True))

config = {}
config['cookie'] = {
    "expiry_days": cookie_data['expiry_days'],
    "key": cookie_data['key'],
    "name": cookie_data['name']
}
config['credentials'] = {"usernames": {}}
for i in user_data:
    config['credentials']['usernames'][i['id']] = {
        "email": i['email'],
        "password": i['password'],
        'failed_login_attempts': i['failed_login_attempts'],
        'last_name': i['last_name'],
        'first_name': i['first_name'],
        "logged_in": i['logged_in'],
    }

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
print(f'session state login.py: {st.session_state}')
print()
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
    st.rerun()
elif st.session_state['authentication_status']:
    if 'user' not in st.session_state:
        st.session_state['user'] = {
            'email': st.session_state['email'],
            'username': st.session_state['username'],
            'name': st.session_state['name'],
            'role': st.session_state['roles']
        }
    st.session_state['authenticator'] = authenticator
    st.switch_page("pages/select.py")
elif st.session_state['authentication_status'] == None:
    if 'customer-insights-platform' in st.session_state['init']:
        authenticator.login(location="main")
        st.rerun()
    else:
        authenticator.login(location="main")

