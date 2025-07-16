# app/main.py

from fastapi import FastAPI, HTTPException
from fastf1.events import get_event_schedule
from fastf1 import get_session
from fastf1 import Cache
from fastf1.core import Laps
from fastapi.middleware.cors import CORSMiddleware

Cache.enable_cache("cache")  # Enable cache directory

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use your domain only
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
                race = get_session(year, race_name, 'Race')
                race.load()
                drivers.update([race.get_driver(d)['FullName'] for d in race.drivers])
            except Exception:
                continue

        return {
            "races": sorted(races),
            "drivers": sorted(drivers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
