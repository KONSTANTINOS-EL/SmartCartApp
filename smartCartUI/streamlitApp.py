import streamlit as st
import pandas as pd
import re

# Load the data from the CSV file.
@st.cache_data
def load_products():
    return pd.read_csv("C:/Μεταπτυχιακό/Python/SmartCartApp/sklavenitis_products.csv", delimiter=';', quotechar='"', on_bad_lines='skip') #csv file from web scraping.

products = load_products()

# Initialize cart in session state,
if "cart" not in st.session_state:
    st.session_state.cart = []

st.title("Smart Cart")

#search bar
search = st.text_input("Search for products:")

if search:
    filtered_products = products[products["name"].str.contains(search, case=False)]
else:
    filtered_products = products

def clean_price(price):
    match =  re.search(r"[\d,]+", price)
    if match:
        number_to_str = match.group(0).replace(",", ".")
        return float(number_to_str)
    return None

#display products in a table
for index, product in filtered_products.iterrows():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(product["image_url"], width=100)
        st.write(f"**{product['name']}**")
        st.write(product["description"])
        price = clean_price(product["price"])
        if price is not None:
            st.write(f"Price: {price:.2f} €")
        else:
            st.write("Price not available")
    with col2:
        if st.button("Add to cart", key=index):
            st.session_state.cart.append(product)
            st.success(f"Added {product['name']} to cart!")

#cart sidebar
st.sidebar.title("Shopping Cart")
total = 0
for item in st.session_state.cart:
    st.sidebar.image(item["image_url"], width=50)
    st.sidebar.write(f"**{item['name']}**")
    price = clean_price(item["price"])
    if price is not None:
        st.sidebar.write(f"Price: {price:.2f} €")
    else:
        st.sidebar.write("Price not available")
    total += price if price is not None else 0
    st.sidebar.write("---")

st.sidebar.write(f"Total: {total:.2f} €")

if st.sidebar.button("Checkout"):
    st.sidebar.success("Checkout successful!")
    st.session_state.cart = []  # Clear the cart after checkout
    st.experimental_rerun()  # Refresh the app to clear the cart display