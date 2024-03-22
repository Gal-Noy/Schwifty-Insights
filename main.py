import os

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

import config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from data import cache
from routes import characters, episodes, locations, insights, auth

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address, default_limits=[os.getenv("RATE_LIMIT")])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(insights.router, prefix="/insights", tags=["insights"])
app.include_router(characters.router, prefix="/characters", tags=["characters"])
app.include_router(episodes.router, prefix="/episodes", tags=["episodes"])
app.include_router(locations.router, prefix="/locations", tags=["locations"])

if __name__ == "__main__":
    cache.cache_data()
    uvicorn.run(app, host="127.0.0.1", port=8000)
