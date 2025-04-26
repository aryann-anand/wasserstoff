from pydantic import BaseModel
from typing import List, Optional

class GuessInput(BaseModel):
    guess: str
    
class GuessResponse(BaseModel):
    success: bool
    message: str
    last_guess: str
    previous_item: str
    score: int
    global_count: int
    game_over: bool
    
class HistoryResponse(BaseModel):
    guesses: List[str]
