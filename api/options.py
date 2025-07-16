from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import fastf1
import os
import joblib
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Enable FastF1 cache (Vercel will allow small temp dir usage)
fastf1.Cache.enable_cache("/tmp/fastf1_cache")

# Load encoder
enc_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'encoders.pkl')
enc = {}
try:
    enc = joblib.load(enc_path)
except Exception as e:
    print(f"[ERROR] Failed to load encoder: {e}")

@app.get("/api/options")
def get_options(year: int = Query(...)):
    print(f"[DEBUG] Received options request for year = {year}")
    drivers = sorted(enc.get("drivers", {}).keys())
    races = []

    try:
        schedule = fastf1.get_event_schedule(year)
        races = schedule["EventName"].dropna().unique().tolist()
        print(f"[DEBUG] Fetched {len(races)} races")
    except Exception as e:
        print(f"[ERROR] Failed to load race schedule: {e}")
    
    return {"drivers": drivers, "races": races}
