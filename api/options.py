from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import fastf1
import os
import joblib

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load encoder
ENC_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'encoders.pkl')
enc = joblib.load(ENC_PATH)

@app.get("/api/options")
def get_options(year: int = Query(...)):
    print(f"[DEBUG] Received options request for year = {year}")
    drivers = sorted(enc.get("drivers", {}).keys())

    races = []
    if year:
        try:
            fastf1.Cache.enable_cache(os.path.join(os.getcwd(), 'fastf1_cache'))
            schedule = fastf1.get_event_schedule(year)
            races = schedule["EventName"].dropna().unique().tolist()
            print(f"[DEBUG] Fetched races: {races}")
        except Exception as e:
            print(f"[ERROR] Failed to fetch race schedule: {e}")

    return {"drivers": drivers, "races": races}
