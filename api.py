from fastapi import FastAPI
from routes import characters, episodes, locations, insights, auth

app = FastAPI()

app.include_router(characters.router, prefix="/characters", tags=["characters"])
app.include_router(episodes.router, prefix="/episodes", tags=["episodes"])
app.include_router(locations.router, prefix="/locations", tags=["locations"])
app.include_router(insights.router, prefix="/insights", tags=["insights"])
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
