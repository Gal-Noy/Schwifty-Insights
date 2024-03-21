import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes import characters, episodes, locations, insights, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters.router, prefix="/characters", tags=["characters"])
# app.include_router(episodes.router, prefix="/episodes", tags=["episodes"])
# app.include_router(locations.router, prefix="/locations", tags=["locations"])
# app.include_router(insights.router, prefix="/insights", tags=["insights"])
# app.include_router(auth.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
