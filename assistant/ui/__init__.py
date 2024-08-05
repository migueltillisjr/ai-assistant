import streamlit as st
#import stripe
import streamlist_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from passlib.context import CryptContext
from streamlit_modal import Modal
from streamlit_option_menu import option_menu
import pandas as pd

# Set up Stripe
# stripe.api_key = 'your_stripe_secret_key'

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def auth():
    st.session_state.sidebar_state='collapsed'
    st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)
    global authenticator, config
    # Load configuration for authentication
    with open(f'/home/miguel/freedom/ai-assistant/ui/config.yaml')
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    global name, authentication_status, username
    name, authentication_status, username = authenticator.login('main', 'main')

    def sign_up():
        model = Modal("Register", key=)