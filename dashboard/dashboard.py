import streamlit as st
import requests
import time

st.set_page_config(page_title="Real-Time Fraud Dashboard", layout="wide")

st.title("🛡️ AI-powered UPI Fraud Detection Dashboard")

st.sidebar.header("Simulation Control")
run_simulation = st.sidebar.checkbox("Run Simulator", value=False)

placeholder = st.empty()

transactions = []

while True:
    if run_simulation:
        # generate random transaction
        import random
        locations = ['Chennai', 'Mumbai', 'Delhi']
        merchants = ['Amazon', 'Flipkart', 'Zomato']

        data = {
            "amount": round(random.uniform(10, 5000), 2),
            "location": random.choice(locations),
            "merchant": random.choice(merchants)
        }

        # call backend
        try:
            res = requests.post("http://127.0.0.1:8000/predict", json=data, timeout=2)
            result = res.json()
            data["fraud"] = result.get("fraud", False)
            transactions.append(data)
        except Exception as e:
            st.error(f"Backend not reachable: {e}")
            time.sleep(2)
            continue

        # display table
        with placeholder.container():
            st.subheader("📊 Latest Transactions")
            df = st.dataframe(transactions[-20:][::-1])  # show last 20, newest first

        time.sleep(2)  # simulate delay
    else:
        st.info("✅ Enable 'Run Simulator' to see real-time data")
        time.sleep(2)
