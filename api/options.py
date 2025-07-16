from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import fastf1
import os
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# ✅ Use a Vercel-friendly cache path
fastf1.Cache.enable_cache("/tmp/fastf1_cache")


@app.get("/api/options")
async def get_options(year: int = Query(...)):
    try:
        print(f"🔧 Received request for year: {year}")

        # ✅ Load encoders
        enc_path = os.path.join(os.path.dirname(__file__), "..", "models", "encoders.pkl")
        enc_path = os.path.abspath(enc_path)
        print(f"🔍 Loading encoder from: {enc_path}")

        if not os.path.exists(enc_path):
            raise FileNotFoundError(f"encoders.pkl not found at {enc_path}")

        enc = joblib.load(enc_path)
        driver_map = enc.get("drivers", {})
        drivers = sorted(driver_map.keys())
        print(f"✅ Loaded {len(drivers)} drivers")

        # ✅ Load event schedule
        try:
            schedule = fastf1.get_event_schedule(year)
            races = schedule["EventName"].dropna().unique().tolist()
            print(f"✅ Loaded {len(races)} races for {year}")
        except Exception as e:
            print(f"[⚠️ Schedule Error] {e}")
            races = []

        return JSONResponse(content={"drivers": drivers, "races": races})

    except Exception as e:
        print(f"[❌ OPTIONS API ERROR] {e}")
        return JSONResponse(
            content={"error": "Internal Server Error", "details": str(e)},
            status_code=500
        )
