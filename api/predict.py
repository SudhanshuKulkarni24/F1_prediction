# api/predict.py

import os
import pickle
import requests
from io import BytesIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

app = FastAPI()

GITHUB_BASE_URL = "https://raw.githubusercontent.com/SudhanshuKulkarni24/F1_prediction/main/models/"

def load_pickle_from_github(filename):
    url = GITHUB_BASE_URL + filename
    r = requests.get(url)
    r.raise_for_status()
    return pickle.load(BytesIO(r.content))

# Load remote model and encoders
try:
    model = load_pickle_from_github("catboost_model.pkl")
    encoder = load_pickle_from_github("encoders.pkl")
except Exception as e:
    print("🛑 Error loading model or encoder:", e)
    model = {}
    encoder = {}

class PredictRequest(BaseModel):
    driver: str
    avg_lap_time: float
    fastest_lap: float

@app.post("/api/predict")
def predict(req: PredictRequest):
    if "drivers" not in encoder or req.driver not in encoder["drivers"]:
        raise HTTPException(status_code=400, detail="Unknown driver")

    driver_encoded = encoder["drivers"][req.driver]
    team_encoded = 0  # If no team data, can be left as zero

    X = np.array([[driver_encoded, team_encoded, req.avg_lap_time, req.fastest_lap]])
    out = {}

    for label in ["Top1", "Top3", "Top5"]:
        clf = model.get(label)
        if clf:
            out[f"{label.lower()}_prob"] = float(clf.predict_proba(X)[0][1])
      # Optional: linearly approximate top3, top5 if only top1 model exists

    reg = model.get("FinalPos")
    if reg:
        pos = reg.predict(X)[0]
        out["predicted_position"] = float(pos)

    return out
