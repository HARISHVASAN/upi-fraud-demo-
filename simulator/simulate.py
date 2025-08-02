import time
import random
import requests
import uuid
from datetime import datetime

API_URL = "http://localhost:8000/predict"  # change if hosted elsewhere

def generate_transaction():
    return {
        "txn_id": str(uuid.uuid4()),
        "amount": round(random.uniform(10, 5000), 2),
        "time": datetime.now().isoformat(),
        "location": random.choice(["Chennai", "Mumbai", "Delhi", "Bangalore"]),
        "merchant": random.choice(["Amazon", "Flipkart", "Zomato", "Swiggy"]),
        "device_id": str(uuid.uuid4())
    }

while True:
    txn = generate_transaction()
    try:
        res = requests.post(API_URL, json=txn)
        print("Sent txn:", txn, "Response:", res.json())
    except Exception as e:
        print("Error:", e)
    time.sleep(2)  # every 2 seconds
