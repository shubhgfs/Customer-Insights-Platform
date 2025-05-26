import os
import dotenv
import bcrypt
import streamlit as st
import streamlit_authenticator as stauth
from azure.cosmos import exceptions
from backend.modules.cosmos_db_connection import get_cosmos_client
import warnings
warnings.filterwarnings("ignore")

dotenv.load_dotenv()

container = get_cosmos_client("Customer Insights Platform", "Users")
# print('session state at start of login.py:', st.session_state)
query = "SELECT * FROM Users u WHERE u.email = 'cookie@gfs.com.au'"
cookie_data = list(container.query_items(query=query, enable_cross_partition_query=True))[0]
# print('cookie_data:', cookie_data)
query = "SELECT * FROM Users u WHERE u.email <> 'cookie@gfs.com.au'"
user_data = list(container.query_items(query=query, enable_cross_partition_query=True))
# print('user_data:', user_data)  
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
# print('config:', config)
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)
# print('authenticator:', authenticator)
# print('st.session_state:', st.session_state)
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
    st.rerun()
elif st.session_state['authentication_status']:
    st.session_state['user'] = {
        'email': st.session_state['email'],
        'username': st.session_state['username'],
        'name': st.session_state['name'],
        'role': st.session_state['roles']
    }
    st.session_state['authenticator'] = authenticator
    print(f'{st.session_state["user"]["name"]} logged in and going to main.py.')
    st.switch_page("pages/main.py")
elif st.session_state['authentication_status'] == None:
    print(f'{st.session_state} before the init code')
    if 'init' in st.session_state and 'customer-insights-platform' in st.session_state['init']:
        authenticator.login(location="main")
        st.rerun()
    else:
        # Initialize 'init' for first-time users if not present
        if 'init' not in st.session_state:
            st.session_state['init'] = {}
        authenticator.login(location="main")

