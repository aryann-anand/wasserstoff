from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongodb import mongodb
from app.db.redis import redis_client

app = FastAPI(title=settings.PROJECT_NAME)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    return response

# Include routers
from app.api.endpoints import game_router
app.include_router(game_router, prefix=f"{settings.API_V1_STR}/game", tags=["game"])


app.include_router(
    game_router.router,
    prefix=f"{settings.API_V1_STR}/game",
    tags=["game"]
)

@app.get("/")
def root():
    return {"message": "Welcome to the What Beats Rock game API!"}
