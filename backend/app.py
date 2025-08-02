from fastapi import FastAPI, Request
import pickle
import numpy as np
import pandas as pd

app = FastAPI()

# Load trained model
xgb_model = pickle.load(open("models/xgboost_model.pkl", "rb"))

@app.get("/")
def root():
    return {"message": "Hello, FastAPI with model is working!"}

@app.post("/predict")
async def predict_fraud(request: Request):
    data = await request.json()
    # data is expected as JSON with keys: amount, location, merchant
    amount = data.get('amount', 100)
    location = data.get('location', 'Chennai')
    merchant = data.get('merchant', 'Amazon')

    # Encode data same way as training
    df = pd.DataFrame([{
        'amount': amount,
        'location': location,
        'merchant': merchant
    }])

    df_encoded = pd.get_dummies(df)
    # Add missing columns (since model expects same columns)
    for col in xgb_model.get_booster().feature_names:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    df_encoded = df_encoded[xgb_model.get_booster().feature_names]
    prediction = xgb_model.predict(df_encoded)

    return {"fraud": bool(prediction[0])}
