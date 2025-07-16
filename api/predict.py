from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import numpy as np
from .load_models import load_models, encoder

# Load all models once
model = load_models()

app = FastAPI()


class PredictRequest(BaseModel):
    year: int
    race: str
    driver: str


@app.get("/api/options")
def get_options(year: Optional[int] = Query(None)):
    import fastf1
    result = {
        "years": list(range(2018, 2025)),  # Customize year range
        "drivers": sorted(encoder["drivers"].keys()),
        "races": []
    }
    try:
        if year:
            schedule = fastf1.get_event_schedule(year)
            result["races"] = schedule["EventName"].dropna().unique().tolist()
    except Exception as e:
        print(f"[!] Failed to load schedule for {year}: {e}")
    return result


@app.post("/api/predict")
def predict(data: PredictRequest):
    import fastf1
    fastf1.Cache.enable_cache("/tmp")  # Vercel writable path

    driver_name = data.driver
    year = data.year
    race = data.race

    if driver_name not in encoder["drivers"]:
        raise HTTPException(status_code=400, detail="Unknown driver name.")

    try:
        event = fastf1.get_event(year, race)
        race_session = event.get_session("Race")
        race_session.load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FastF1 load failed: {e}")

    abbrev = encoder["driver_abbr"].get(driver_name)
    if not abbrev:
        raise HTTPException(status_code=400, detail="Abbreviation missing for driver.")

    try:
        laps = race_session.laps.pick_driver(abbrev)
        if laps.empty:
            raise HTTPException(status_code=404, detail="No lap data found.")
        avg_lap = laps["LapTime"].mean().total_seconds()
        fastest_lap = laps["LapTime"].min().total_seconds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lap time extraction failed: {e}")

    driver_encoded = encoder["drivers"][driver_name]
    team_encoded = 0  # Team info not available
    X = np.array([[driver_encoded, team_encoded, avg_lap, fastest_lap]])

    output = {}
    for label in ["Top1", "Top3", "Top5"]:
        clf = model.get(label)
        if clf:
            output[f"{label.lower()}_prob"] = float(clf.predict_proba(X)[0][1])

    reg = model.get("FinalPos")
    if reg:
        output["predicted_position"] = float(reg.predict(X)[0])

    return output
