# api/predict.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import fastf1
from fastapi.responses import JSONResponse
import joblib
import pandas as pd
import os

# === FastAPI app ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Load models & encoders ===
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models")
model = joblib.load(os.path.join(MODEL_PATH, "catboost_model.pkl"))
encoders = joblib.load(os.path.join(MODEL_PATH, "encoders.pkl"))

# === Options Endpoint ===
@app.get("/api/options")
def get_options(year: int = Query(None)):
    try:
        drivers = sorted(encoders["drivers"].keys())
    except:
        drivers = []

    races = []
    if year:
        try:
            fastf1.Cache.enable_cache(os.path.join(os.path.dirname(__file__), "..", "cache"))
            schedule = fastf1.get_event_schedule(year)
            races = schedule["EventName"].dropna().unique().tolist()
        except Exception as e:
            print(f"❌ Error loading schedule for {year}: {e}")

    return {"drivers": drivers, "races": races}

# === Predict Endpoint ===
@app.post("/api/predict")
def predict(request: dict):
    try:
        driver = request.get("driver")
        race = request.get("race")
        year = int(request.get("year"))

        # Encoding
        driver_encoded = encoders["driver_encoder"].transform([driver])[0]

        # Dummy features — real model should use real lap data
        avg_lap = 90.0
        fastest_lap = 85.0

        features = pd.DataFrame([{
            "DriverEncoded": driver_encoded,
            "TeamEncoded": 0,  # Removed team handling
            "AvgLapTime": avg_lap,
            "FastestLap": fastest_lap
        }])

        probs = model.predict_proba(features)
        top1_prob = round(probs[0][1] * 100, 2)

        return {
            "driver": driver,
            "race": race,
            "year": year,
            "Top1": f"{top1_prob}%",
            "Top3": f"{round(top1_prob * 1.5, 2)}%",
            "Top5": f"{round(top1_prob * 2, 2)}%"
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
