from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import fastf1
import os
import joblib
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# ✅ Vercel-safe cache
fastf1.Cache.enable_cache("/tmp/fastf1_cache")

@app.get("/api/options")
async def get_options(year: int = Query(...)):
    try:
        print(f"📩 Received request for year: {year}")

        # Load encoders
        enc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "encoders.pkl"))
        print(f"📦 Loading encoders from {enc_path}")

        if not os.path.exists(enc_path):
            raise FileNotFoundError(f"Missing encoders.pkl at {enc_path}")

        enc = joblib.load(enc_path)
        drivers = sorted(enc.get("drivers", {}).keys())
        print(f"✅ Found {len(drivers)} drivers")

        try:
            schedule = fastf1.get_event_schedule(year)
            races = schedule["EventName"].dropna().unique().tolist()
            print(f"✅ Loaded {len(races)} races for {year}")
        except Exception as e:
            print(f"⚠️ Race loading failed: {e}")
            races = []

        return JSONResponse(content={"drivers": drivers, "races": races})

    except Exception as e:
        print(f"❌ Exception in /api/options: {e}")
        traceback.print_exc()
        return JSONResponse(
            content={"error": "Internal Server Error", "details": str(e)},
            status_code=500
        )
