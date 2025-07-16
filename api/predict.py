# api/predict.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests, pickle
from io import BytesIO
import numpy as np

app = FastAPI()

MODEL_URL = "https://raw.githubusercontent.com/SudhanshuKulkarni24/F1_prediction/main/models/catboost_model.pkl"
ENC_URL = "https://raw.githubusercontent.com/SudhanshuKulkarni24/F1_prediction/main/models/encoders.pkl"

def load_remote_model():
    r = requests.get(MODEL_URL); r.raise_for_status()
    return pickle.load(BytesIO(r.content))

def load_remote_encoders():
    r = requests.get(ENC_URL); r.raise_for_status()
    return pickle.load(BytesIO(r.content))

model = load_remote_model()
enc = load_remote_encoders()

class Input(BaseModel):
    driver: str
    avg_lap_time: float
    fastest_lap: float

@app.post("/api/predict")
def predict(data: Input):
    de = enc["drivers"].get(data.driver)
    if de is None:
        raise HTTPException(status_code=400, detail="Unknown driver")
    X = np.array([[de, data.avg_lap_time, data.fastest_lap]])
    top1 = model["Top1"].predict_proba(X)[0][1]
    top3 = model["Top3"].predict_proba(X)[0][1]
    top5 = model["Top5"].predict_proba(X)[0][1]
    pos = float(model["FinalPos"].predict(X)[0])
    return {
        "Top1_prob": top1,
        "Top3_prob": top3,
        "Top5_prob": top5,
        "Predicted_Position": pos
    }
