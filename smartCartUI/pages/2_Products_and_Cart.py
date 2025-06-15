import streamlit as st
import pandas as pd
import requests

API_URL = 'http://smartcart-backend:5000'

if not st.session_state.get("token") or not st.session_state.get("user_id"):
    st.warning("Πρέπει να συνδεθείς πρώτα.")
    st.stop()

#Debugging
# st.write("token: ", st.session_state.get("token"))
# st.write("user_id", st.session_state.get("user_id"))  

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
    
def get_cart():
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    post_data = {

        "user_id": st.session_state.user_id
    }
    res = requests.post(f"{API_URL}/carts/get_cart", json=post_data ,headers=headers)
    if res.status_code == 200:
        return res.json().get("products", [])
    else:
        print("Error fetcing cart:", res.text)
        return []
    

def purchase_cart():
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    post_data = {

        "user_id": st.session_state.user_id
    }
    res = requests.post(f"{API_URL}/purchase", json=post_data ,headers=headers)
    if res.status_code == 200:
        return res.json().get("products", [])
    else:
        print("Error fetcing cart:", res.text)
        return []
    
def delete_all_products():
    res = requests.delete(f"{API_URL}/products")
    if res.status_code == 200:
        st.success(res.json().get("message", "Τα προϊόντα διαγράφηκαν."))

def delete_product_from_cart(product_id):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    json_body_data = {
        "user_id": st.session_state.user_id
    }
    res = requests.delete(f"{API_URL}/cart/delete_product_from_cart/{product_id}", json=json_body_data, headers=headers)
    if res.status_code == 200:
        st.success(res.json().get("message", "Το προϊόν αφαιρέθηκε από το καλάθι."))


st.title("Βρές τα προϊόντα που χρειάζεσαι και πρόσθεσε τα στο καλάθι σου!")
query = st.text_input("Αναζήτηση προϊόντος:")

if st.button("Αναζήτηση"):
    requests.post(f"{API_URL}/serach-product-sklavenitis", json={"query": query})
    requests.post(f"{API_URL}/serach-product-marketin", json={"query": query})

#Products View
res = requests.get(f"{API_URL}/products")
products = res.json()
df = pd.DataFrame(products)

if st.button("Διαγραφή όλων των προϊόντων"):
    confirm = st.checkbox("Είμαι σίγουρος ότι θέλω να διαγράψω όλα τα προϊόντα του καλαθιού")
    if confirm:
        delete_all_products()
        st.rerun()
    else:
        st.warning("Επιβεβαίωσε πριν προχωρήσεις.")

for index, row in df.iterrows():
    st.image(row.get("image_url"), width=150)
    st.write(f"**{row['name']}** - {row['price']}€")
    st.write(f"{row['description']}")
    if st.button("Προσθήκη στο καλάθι", key=f"{row['name']}_{index}"):
        result = add_to_cart(row["_id"], quantity=1)
        if result:
            st.success(f"Το προϊόν προστέθηκε στο καλάθι επιτυχώς!")
        else:
            st.error("Αποτυχία προσθήκης.")
			
st.sidebar.subheader("Καλάθη")
cart_items = get_cart()
total_cost = 0

if cart_items:
    for item in cart_items:
        name = item["name"]
        quantity = item["quantity"]
        price = float(item["price"])
        total = price * quantity
        total_cost += total

        st.sidebar.write(f"**{name}**")
        st.sidebar.write(f"Ποσότητα: {quantity} - {price}€ x {quantity} = {total:.2f}€")
        if st.sidebar.button("Αφαίρεση", key=f"delete_{item['product_id']}"):
            delete_product_from_cart(item["product_id"])
        else:
            st.error("Αποτυχία αφαίρεσης από την λίστα προϊόντων")
        st.sidebar.markdown("---")
    st.sidebar.markdown(f"## Συνολικό Κόστος: {total_cost:.2f}€")

    if st.sidebar.button("Ολοκλήρωση Αγοράς"):
        result = purchase_cart()
        if result:
            st.sidebar.success("Η αγορά ολοκληρώυηκε με επιτυχία.")
            #Για να αδείασει το καλάθι και να ενημερωθεί
            st.rerun()
else:
    st.info("Το καλάθι σας είναι άδειο.")
