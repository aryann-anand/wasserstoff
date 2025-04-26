from fastapi import APIRouter, HTTPException, Depends, Request, Header
from typing import Optional
from ...models.game import GuessInput, GuessResponse, HistoryResponse
from ...services.game_service import game_service

router = APIRouter()

@router.post("/guess", response_model=GuessResponse)
async def make_guess(
    request: Request,
    guess_input: GuessInput,
    persona: Optional[str] = Header("serious")
):
    session_id = request.cookies.get("session_id")
    
    if persona not in ["serious", "cheery"]:
        persona = "serious"
    
    result = await game_service.process_guess(session_id, guess_input.guess, persona)
    return result

@router.get("/history", response_model=HistoryResponse)
async def get_history(request: Request, limit: int = 5):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="No active game found")
    history = game_service.get_history(session_id, limit)
    return HistoryResponse(guesses=history)

@router.post("/reset")
async def reset_game(request: Request):
    session_id = request.cookies.get("session_id")
    game_service.reset_game(session_id)
    return {"message": "Game has been reset"}
