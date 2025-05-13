import streamlit as st
import pandas as pd
import requests
import re

CSV_URL = "C:/Μεταπτυχιακό/Python/SmartCartApp/sklavenitis_products.csv"
API_URL = "http://127.0.0.1:5000"

@st.cache_data
#------------------- All Functions---------------------------
def register(username, email, passrord):
    res = requests.post(f'{API_URL}/users/register', json={"username": username, "email": email, "password": passrord})
    return res.status_code == 201

def login(email, password):
    login_url = "http://localhost:5000/users/login"
    res = requests.post(login_url, json={"email": email, "password": password})
    if res.status_code == 200:
        return res.json().get('token')
    else:
        print("Login error: ", res.text)
        return None

def web_scraping_sklavenitis(query):
    query = str(query)
    res = requests.post(f"{API_URL}/serach-product-sklavenitis", json={"query": query})
    return res.json()

def web_scraping_marketin(query):
    query = str(query)
    res = requests.post(f"{API_URL}/serach-product-marketin", json={"query": query})
    return res.json()

def fetch_products_from_db():
    res = requests.get(f"{API_URL}/products")
    return res.json()

# UI App.
st.set_page_config(page_title="Smart Cart for your shopping", layout="wide")
st.title("Smart Cart Supermarket")

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
            token = login(email, password)
            if token:
                st.session_state.token = token
                st.success("Login successful!")
                st.rerun()
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
else:
    #App after login
    st.subheader("Αναζήτηση Προϊόντων από Supermarket")
    query = st.text("Πληκτρολόγησε ένα προϊόν..")

    if st.button("Αναζήτηση"):
        with st.spinner("Αναζήτηση σε εξέλιξη..."):
            sklav_results = web_scraping_sklavenitis(query)
            marketin_result = web_scraping_marketin(query)
            st.success("Τα προϊόντα αποθηκεύτηκαν")

    #Load products from products collection
    products = fetch_products_from_db()

    if products:
       # Δημιουργία του DataFrame
        df = pd.DataFrame(products)

        # Εμφάνιση των προϊόντων με στήλες
        st.dataframe(df[['name', 'price', 'description', 'image_url']])
        
        # Εμφάνιση εικόνας προϊόντος (προαιρετικό)
        if 'image_url' in df.columns:
            for index, row in df.iterrows():
                st.image(row['image_url'], caption=row['name'], use_column_width=True)
    else:
        st.info("Δεν βρέθηκαν προϊόντα για την αναζήτησή σας.")


        



