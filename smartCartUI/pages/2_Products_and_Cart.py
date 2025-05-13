import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:5000"

def add_to_cart(product_id, quantity = 1):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    load_data = {
        "user_id" : st.session_state.user_id,
        "product_id": product_id,
        "quantity": quantity
    }

    res = requests.post(f"{API_URL}/carts/add_product", json=load_data, headers=headers)
    if res.status_code == 200:
        return res.json()

st.title("Βρές τα προϊόντα που χρειάζεσαι και πρόσθεσε τα στο καλάθι σου!")
query = st.text_input("Αναζήτηση προϊόντος:")

if st.button("Αναζήτηση"):
    requests.post(f"{API_URL}/serach-product-sklavenitis", json={"query": query})
    requests.post(f"{API_URL}/serach-product-marketin", json={"query": query})

#Products View
res = requests.get(f"{API_URL}/products")
products = res.json()
df = pd.DataFrame(products)

for index, row in df.iterrows():
    st.image(row.get("image_url"), width=150)
    st.write(f"**{row["name"]}** - {row["price"]}€")
    st.write(f"{row["description"]}")
    if st.button("Προσθήκη στο καλάθι", key=f"{row["name"]}_{index}"):
        result = add_to_cart(row["_id"], quantity=1)
        if result:
            st.success(f"Το προϊόν προστέθηκε στο καλάθι επιτυχώς!")
        else:
            st.error("Αποτυχία προσθήκης.")
