import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = 'http://smartcart-backend:5000'

if not st.session_state.get("token") or not st.session_state.get("user_id"):
    st.warning("Πρέπει να συνδεθείς πρώτα.")
    st.stop()


headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

#User statistics for top 5 products
st.title("Στατιστικά Αγορών Χρήστη")

res = requests.get(f"{API_URL}/api/analysis/user_purchases", headers=headers)

if res.status_code == 200:
    stats = res.json()

    st.metric("Συνολικές Αγορές", stats["total_purchases"])
    st.metric("Συνολικό ξόδεμα", f"{stats["total_spent"]}€")

    top_five = stats["top_5_products"]
    purchases_time = stats.get("purchases_over_time", [])

    if top_five:
        df_top = pd.DataFrame({
            "Προϊόν": top_five,
            "Πλήθος": [1]*len(top_five)
        })

        fig_bar =  px.bar(df_top, x="Προϊόν", y="Πλήθος", title="Top 5 Προϊόντα", color="Προϊόν")
        st.plotly_chart(fig_bar)
    else:
        st.info("Δεν υπάρχουν αρκετά δεδομένα")
else:
    st.error("Αποτυχία φόρτωσης στατιστικών")    

#Products predictions
st.subheader("Προβλεπόμενα προϊόντα")

res_predict = requests.get(f"{API_URL}/api/analysis/predict_next", headers=headers)\

if res_predict.status_code == 200: 
    preds = res_predict.json()["predicted_products"]

    if preds:
        for p in preds: 
            st.markdown(f"-{p}")
    else:
        st.info("Δεν υπάρχουν ακόμα προτεινόμενα προϊόντα")
else:
    st.error("Σφάλαμα στις προβλέψεις")


st.subheader("Συχνά Αγοραζόμενα Μαζί")

#Product choice
res_all_products = requests.get(f"{API_URL}/products")
if res_all_products.status_code == 200:
    product_data = res_all_products.json()
    product_dict = {prod["name"]: prod["_id"] for prod in product_data}
    selected = st.selectbox("Επιλέξτε προϊόν: ", options=list(product_dict.keys()))

    if st.button("Δές σχετικά προϊόντα"):
        pid = product_dict[selected]
        res_freq = requests.get(f"{API_URL}/api/analysis/frequently-bought-togehter/{pid}")
        if res_freq == 200:
            related = res_freq.json()["frequently_bought_together"]
            if related:
                st.markdown("**Αγοράζονται συχνά μαζι με:**")
                for r in related:
                    st.markdown(f"-{r}")
            else:
                st.info("Δεν υπάρχουν σχετικά προϊόντα.")
        else:
            st.error("Αποτυχία φόρτωσης συσχετιζόμενων προϊόντων.")
    else:
        st.warning("Δεν υπάρχουν προϊόντα")