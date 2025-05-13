import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page



API_URL = "http://localhost:5000"

@st.cache_data

#Login/Register Functions
def register(username, email, passrord):
    res = requests.post(f'{API_URL}/users/register', json={"username": username, "email": email, "password": passrord})
    return res.status_code == 201

def login(email, password):
    res = requests.post(f"{API_URL}/users/login", json={"email": email, "password": password})
    if res.status_code == 200:
        data_res = res.json()
        token = data_res.get("token")
        user = data_res.get("user")
        user_id = user.get("_id") if user else None
        return token, user_id
    else:
        print("Login error: ", res.text)
        return None, None
    
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

auth_tab = st.sidebar.radio("Authentication", ["Login", "Register"])

if st.session_state.token is None:
    if auth_tab == "Login":
        st.subheader("Login")
        email = st.text_input("Email")

        if email and '@' not in email:
            st.warning("Please enter a valid email address")

        password = st.text_input("Password", type="password")
        if not password:
            st.warning("Please enter a valid password address")

        if st.button("Login"):
            token, user_id = login(email, password)
            if token and user_id:
                st.session_state.token = token
                st.session_state.user_id = user_id
                st.success("Login successful!")
                st.switch_page("pages/2_Products_and_Cart.py")
            else:
                st.error("Login failed. Please check your credentials.")
    else:
        st.subheader("Register")
        reg_username = st.text_input("New Username")

        reg_email = st.text_input("Email")
        reg_password = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register(reg_username, reg_email, reg_password):
                st.success("Registration successful! You can now login.")
            else:
                st.error("Registration failed. Please try again.")
    

