import streamlit as st
import requests
import time
import random
from datetime import datetime

st.set_page_config(page_title="Real-Time Fraud Dashboard", layout="wide")

st.title("🛡️ AI-powered UPI Fraud Detection Dashboard")

st.sidebar.header("Simulation Control")
run_simulation = st.sidebar.checkbox("Run Simulator", value=False)

placeholder = st.empty()
transactions = []

# Counter to inject fraud every N transactions
counter = 0
N = 8  # every 8th transaction will look suspicious

while True:
    if run_simulation:
        counter += 1

        # normally safe transaction
        data = {
            "amount": round(random.uniform(10, 5000), 2),
            "location": random.choice(['Chennai', 'Mumbai', 'Delhi']),
            "merchant": random.choice(['Amazon', 'Flipkart', 'Zomato']),
            "hour": datetime.now().hour  # add hour feature
        }

        # Inject suspicious pattern every Nth transaction
        if counter % N == 0:
            data["amount"] = random.choice([8999, 9999])  # unusually large amount
            data["merchant"] = "UnknownMerchant"
            data["location"] = "UnknownCity"
            data["hour"] = 2  # suspicious hour

        try:
            backend_url = "https://upi-fraud-demo.onrender.com/"  # replace!
            res = requests.post(backend_url, json=data)
            result = res.json()
            data["fraud"] = result.get("fraud", False)
            transactions.append(data)
        except Exception as e:
            st.error(f"Backend not reachable: {e}")
            time.sleep(2)
            continue

        # Show latest transactions
        with placeholder.container():
            st.subheader("📊 Latest Transactions")
            st.dataframe(transactions[-20:][::-1])  # newest first

        time.sleep(2)  # simulate real stream
    else:
        st.info("✅ Enable 'Run Simulator' to see real-time fraud detection")
        time.sleep(2)
