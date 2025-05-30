from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uuid

from .api.endpoints import game
from .core.config import settings
from .db.mongodb import mongodb
from .db.redis import redis_client

app = FastAPI(title=settings.PROJECT_NAME)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://wasserstoff-aryan.vercel.app",
        "https://wasserstoff-aryans-projects-f221096b.vercel.app",
        "https://wasserstoff-git-main-aryans-projects-f221096b.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"]
)


# Event handlers for database connections
@app.on_event("startup")
async def startup_db_client():
    await mongodb.connect_to_mongodb()
    await redis_client.connect_to_redis()

@app.on_event("shutdown")
async def shutdown_db_client():
    await mongodb.close_mongodb_connection()
    await redis_client.close_redis_connection()

# Middleware to set session cookies
@app.middleware("http")
async def add_session_cookie(request: Request, call_next):
    response = await call_next(request)
    
    # If no session ID is found, set a new one
    if not request.cookies.get("session_id"):
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key="session_id", 
            value=session_id, 
            httponly=True,
            samesite="None",  # Important for cross-domain requests
            secure=True       # Required with SameSite=None
        )
    
    return response

# Include routers
app.include_router(game.router, prefix=f"{settings.API_V1_STR}/game", tags=["game"])

@app.get("/")
def root():
    return {"message": "© Aryan Anand 2025 , https://github.com/aryann-anand . Welcome to the What Beats Rock API!"}
