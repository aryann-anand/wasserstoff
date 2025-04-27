from fastapi import APIRouter, HTTPException, Depends, Request, Header
from typing import Optional
from ...models.game import GuessInput, GuessResponse, HistoryResponse
from ...services.game_service import game_service

router = APIRouter()

@router.post("/guess", response_model=GuessResponse)
async def make_guess(
    request: Request,
    guess_input: GuessInput,
    persona: Optional[str] = Header("cheery")
):
    # Extract session ID from cookies or create a new one
    session_id = request.cookies.get("session_id")
    
    # Validate persona
    if persona not in ["serious", "cheery"]:
        persona = "cheery"
    
    # Process the guess
    result = await game_service.process_guess(
        session_id=session_id,
        guess=guess_input.guess,
        persona=persona
    )
    
    # Create response
    response = GuessResponse(
        success=result["success"],
        message=result["message"],
        last_guess=result["last_guess"],
        previous_item=result["previous_item"],
        score=result["score"],
        global_count=result["global_count"],
        game_over=result["game_over"]
    )
    
    return response

@router.get("/history", response_model=HistoryResponse)
async def get_history(request: Request, limit: int = 5):
    session_id = request.cookies.get("session_id")
    if not session_id:
        # Return empty history instead of error
        return HistoryResponse(guesses=[])
    
    history = game_service.get_history(session_id, limit)
    return HistoryResponse(guesses=history)

@router.post("/reset")
async def reset_game(request: Request):
    # Extract session ID from cookies or create a new one
    session_id = request.cookies.get("session_id")
    
    # Reset the game
    game_service.reset_game(session_id)
    
    return {"message": "Game has been reset"}
