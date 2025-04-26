from pydantic_settings import BaseSettings
from typing import ClassVar
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "What Beats Rock Game"
    
    # MongoDB settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "whatbeatsrock")
    
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    
    # Gemini settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Game settings
    STARTING_WORD: str = "Rock"
    
    # Persona settings
    class PersonasConfig:
        arbitrary_types_allowed = True
        
    PERSONAS: ClassVar[dict] = {
        "serious": {
            "positive_response": "Correct. '{}' beats '{}'. This answer has been given {} times before.",
            "negative_response": "Incorrect. '{}' does not beat '{}'. Game over. Your score: {}",
            "duplicate_response": "Game over. '{}' has already been guessed. Your score: {}"
        },
        "cheery": {
            "positive_response": "Awesome! '{}' totally beats '{}' 🎉! This clever answer has been used {} times!",
            "negative_response": "Oops! '{}' doesn't beat '{}' 😢. Game over! Your score: {}",
            "duplicate_response": "Oh no! '{}' has already been guessed! 🙈 Game over! Your score: {}"
        }
    }

settings = Settings()
