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

backend_url = "https://upi-fraud-demo.onrender.com/"  # replace with your actual backend URL

while True:
    if run_simulation:
        # Generate random transaction
        locations = ['Chennai', 'Mumbai', 'Delhi']
        merchants = ['Amazon', 'Flipkart', 'Zomato']

        data = {
            "amount": round(random.uniform(10, 5000), 2),
            "location": random.choice(locations),
            "merchant": random.choice(merchants)
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

        # Display table
        with placeholder.container():
            st.subheader("📊 Latest Transactions")
            st.dataframe(transactions[-20:][::-1])  # show last 20, newest first

        time.sleep(2)  # simulate delay
    else:
        st.info("✅ Enable 'Run Simulator' to see real-time data")
        time.sleep(2)
