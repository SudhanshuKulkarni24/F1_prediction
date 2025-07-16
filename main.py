import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastf1 import get_session, get_event_schedule, Cache

# ✅ Ensure 'cache' folder exists (Railway doesn't persist folders from repo)
os.makedirs("cache", exist_ok=True)
Cache.enable_cache("cache")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/options")
def get_options(year: int):
    try:
        schedule = get_event_schedule(year)
        races = list(schedule['EventName'].unique())
        drivers = set()

        for race_name in races:
            try:
                session = get_session(year, race_name, 'Race')
                session.load()
                drivers.update([session.get_driver(d)['FullName'] for d in session.drivers])
            except Exception:
                continue

        return {
            "races": sorted(races),
            "drivers": sorted(drivers)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
