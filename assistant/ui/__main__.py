import streamlit as st
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from passlib.context import CryptContext
from streamlit_modal import Modal
from streamlit_option_menu import option_menu
import pandas as pd
from io import StringIO
import sys

current_script_directory = os.path.abspath(os.path.dirname(__file__))
two_levels_up = os.path.dirname(os.path.dirname(current_script_directory))
sys.path.append(two_levels_up)
from assistant import Assistant
from assistant.config import *

FINE_TUNING = os.getenv('FINE_TUNING')

# Set up Stripe (if needed)
# import stripe
# stripe.api_key = 'your_stripe_secret_key'

def load_config():
    config_path = os.path.expanduser('~/.assistant/config.yaml')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_ui_auth():
    config = load_config()
    ui_auth = config.get('ui_auth')
    if ui_auth is None:
        raise KeyError("Key 'ui_auth' not found in the config file")
    return ui_auth

UI_AUTH_FILE = get_ui_auth()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def auth():
    global authenticator, config, authentication_status
    
    with open(UI_AUTH_FILE) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    global name, username
    name, authentication_status, username = authenticator.login('main', 'main')
    
    # Display the image only if not authenticated
    if authentication_status is None:
        st.image(config['image_dir'] + '/adler2.png', use_column_width=True)

def sign_up():
    modal = Modal("Register", key="signup-modal")
    open_modal = st.button("Sign Up")
    if open_modal:
        modal.open()
    if modal.is_open():
        with modal.container():
            new_user_email = st.text_input('Email')
            new_user_username = st.text_input('Username')
            new_user_password = st.text_input('Password', type='password')
            new_user_subscription = st.selectbox('Subscription Type', ['basic', 'premium'])
            if st.button('Register'):
                if new_user_username in config['credentials']['usernames']:
                    st.error('Username already exists')
                else:
                    hashed_password = pwd_context.hash(new_user_password)
                    config['credentials']['usernames'][new_user_username] = {
                        'name': new_user_username,
                        'email': new_user_email,
                        'password': hashed_password,
                        'subscription': new_user_subscription,
                    }
                    with open(UI_AUTH_FILE, 'w') as file:
                        yaml.dump(config, file)
                    st.success('User registered successfully!')

def save_uploaded_file(uploaded_file, save_path):
    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False

def auth_success():
    with st.sidebar:
        st.image(config['image_dir'] + '/adler2.png', use_column_width=True)
        selected_option = option_menu(
            "Main Menu",
            ["Home", "Profile"],
            icons=["house", "person", "door"],
            menu_icon="cast",
            default_index=0,
        )
        authenticator.logout('Logout', 'main')

    if selected_option == "Home":
        st.title("Home Page")
        uploaded_files = st.file_uploader("Upload files", type=("csv", "pdf"), accept_multiple_files=True)
        prompt = st.text_input(
            "Ask something about your data",
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_files,
        )
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if '.csv' in uploaded_file.name:
                    df = pd.read_csv(uploaded_file)
                    st.write(uploaded_file.name)
                    st.write(df)
                    save_path = FINE_TUNING + '/original/' + uploaded_file.name
                    save_uploaded_file(uploaded_file=uploaded_file, save_path=save_path)
                if '.pdf' in uploaded_file.name:
                    save_path = FINE_TUNING + '/original/' + uploaded_file.name
                    save_uploaded_file(uploaded_file=uploaded_file, save_path=save_path)
        if uploaded_files and prompt:
            with st.spinner("Processing..."):
                AI = Assistant()
                AI.send_message(prompt)
                response = AI.wait_on_run()
                response = response.strip("[]'")
                st.write(response)
            st.success("Processing completed successfully!")

    elif selected_option == "Profile":
        st.title("Profile Page")
        st.title("Account Details")
        st.write(f"Welcome *{name}*")

        email = st.text_input('Email', value=config['credentials']['usernames'][username]['email'])
        amount = st.number_input('Amount', min_value=0.0, step=0.01)

        st.subheader('Update User Details')
        new_email = st.text_input('New Email', value=email)
        new_username = st.text_input('New Username', value=username)
        new_password = st.text_input('New Password', type='password')
        subscription_type = st.selectbox(
            'Subscription Type', 
            ['basic', 'premium'], 
            index=['basic', 'premium'].index(
                config['credentials']['usernames'][username]['subscription']
                ))

        if st.button('Update Details'):
            config['credentials']['usernames'][username]['email'] = new_email
            config['credentials']['usernames'][username]['name'] = new_username
            if new_password:
                config['credentials']['usernames'][username]['password'] = pwd_context.hash(new_password)
            config['credentials']['usernames'][username]['subscription'] = subscription_type
            with open(UI_AUTH_FILE, 'w') as file:
                yaml.dump(config, file)
            st.success('Details updated successfully')

def main():
    auth()
    if authentication_status:
        auth_success()
    elif authentication_status == False:
        st.error('Username/password is incorrect')
        sign_up()
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        sign_up()

main()
