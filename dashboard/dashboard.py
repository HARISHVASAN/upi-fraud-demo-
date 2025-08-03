import streamlit as st
import requests
import time
import random

st.set_page_config(page_title="Real-Time Fraud Dashboard", layout="wide")

st.title("🛡️ AI-powered UPI Fraud Detection Dashboard")

st.sidebar.header("Simulation Control")
run_simulation = st.sidebar.checkbox("Run Simulator", value=False)

placeholder = st.empty()
transactions = []

# ✅ Replace this with your actual Render backend URL
backend_url = "https://upi-fraud-demo.onrender.com/"

while True:
    if run_simulation:
        # Normal random transaction
        locations = ['Chennai', 'Mumbai', 'Delhi']
        merchants = ['Amazon', 'Flipkart', 'Zomato']

        data = {
            "amount": round(random.uniform(10, 5000), 2),
            "location": random.choice(locations),
            "merchant": random.choice(merchants)
        }

        # 🚨 Force fraud every 10 transactions
        if len(transactions) % 10 == 0 and len(transactions) != 0:
            data = {
                "amount": 9999,  # suspiciously high amount
                "location": "Delhi",
                "merchant": "UnknownMerchant"
            }

        # Call backend
        try:
            res = requests.post(backend_url, json=data)
            result = res.json()
            data["fraud"] = result.get("fraud", False)
            transactions.append(data)
        except Exception as e:
            st.error(f"❌ Backend not reachable: {e}")
            time.sleep(2)
            continue

        # Display latest transactions table
        with placeholder.container():
            st.subheader("📊 Latest Transactions (newest first)")
            st.dataframe(transactions[-20:][::-1])

        time.sleep(2)  # simulate delay between transactions

    else:
        st.info("✅ Enable 'Run Simulator' to see real-time transactions")
        time.sleep(2)
