import streamlit as st
import os
#import stripe
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


# Set up Stripe
# stripe.api_key = 'your_stripe_secret_key'

def load_config():
    # Expand the user path and read the YAML file
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
    st.session_state.sidebar_state='collapsed'
    st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)
    global authenticator, config
    # Load configuration for authentication
    with open(UI_AUTH_FILE) as file:
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
    # Initialize the modal
    modal = Modal("Register", key="signup-modal")

    # Button to open the modal
    open_modal = st.button("Sign Up")

    if open_modal:
        modal.open()

    # Define the modal content
    if modal.is_open():
        with modal.container():
            # Sign-up page
            # st.title('Register')
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


def upload_files():
    st.title("File Q&A with OpenAi")
    uploaded_files = st.file_uploader("Upload an article", type=("csv", "pdf"), accept_multiple_files=True)
    question = st.text_input(
        "Ask something about the article",
        placeholder="Can  you give me a short summary?",
        disabled=not uploaded_files,
    )

    if uploaded_files:
        # Iterate over the list of uploaded files and process them
        for uploaded_file in uploaded_files:
            #upload to assistant
            pass
    if uploaded_files and question:
        # make query to assistant & write response to view
        #st.write(message)
        pass

def auth_success():
    with st.sidebar:
        selected_option = option_menu(
            "Main Menu",
            ["Home", "Profile"],
            icons=["house", "person", "door"],
            menu_icon="cast",
            default_index=0,
        )
        authenticator.logout('Logout', 'main')
    if selected_option =="Home":
        st.title("Home Page")
        uploaded_files = st.file_uploader("Upload files", type=("csv", "pdf"), accept_multiple_files=True)
        prompt = st.text_input(
            "Ask something about the article",
            placeholder="Can  you give me a short summary?",
            disabled=not uploaded_files,
        )
        if uploaded_files:
            # Read the CSV file into a DataFrame
            # df = pd.read_csv(uploaded_file)
            # Display the DataFrame
            # st.write(df)
            pass
        if uploaded_files and prompt:
            pass


    elif selected_option == "Profile":
        st.title("Profile Page")
        st.title("Account Details")
        st.write(f"Welcome *{name}*")

        # Collect user information
        email = st.text_input('Email', value=config['credentials']['usernames'][username]['email'])
        amount = st.number_input('Amount', min_value=0.0, step=0.01)

        # User detail update pane
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

            # # Add code to update suscription
            # try:
            #     customer = stripe.Customer.create(email=email)

            #     # create a payment intent
            #     payment_intent = stripe.PaymentIntent.create(
            #         amount=int(amount * 100), # Amouhnt in cents
            #         currency='usd',
            #         customer=customer.id,
            #         description='SaaS subscription',
            #     )
            # except Exception as e:
            #     st.error(f'Error: {e}')
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
