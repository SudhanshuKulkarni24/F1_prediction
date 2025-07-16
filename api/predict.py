import joblib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# Load model and encoder
model = joblib.load("models/catboost_model.pkl")
encoder = joblib.load("models/encoders.pkl")

class PredictRequest(BaseModel):
    driver: str
    avg_lap_time: float
    fastest_lap: float

@app.post("/api/predict")
async def predict(req: PredictRequest):
    driver = req.driver
    avg_lap = req.avg_lap_time
    fast_lap = req.fastest_lap

    if driver not in encoder["drivers"]:
        return JSONResponse(status_code=400, content={"error": "Unknown driver"})

    driver_encoded = encoder["drivers"][driver]
    team_encoded = 0  # Assuming team is not present

    X = np.array([[driver_encoded, team_encoded, avg_lap, fast_lap]])

    probs = model.predict_proba(X)
    final_pos = model.predict(X)[0]

    return {
        "Top1_prob": float(probs[0][1]),
        "Top3_prob": float(min(probs[0][1] + 0.2, 1.0)),
        "Top5_prob": float(min(probs[0][1] + 0.4, 1.0)),
        "FinalPos": int(final_pos)
    }