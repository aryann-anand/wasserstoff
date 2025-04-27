from fastapi import APIRouter, HTTPException, Depends, Request, Response, Header
from typing import Optional
import uuid
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
    
    # Create new session if none exists
    response_object = None
    if not session_id:
        session_id = str(uuid.uuid4())
        response_object = Response()
        response_object.set_cookie(
            key="session_id", 
            value=session_id, 
            httponly=True,
            samesite="None",
            secure=True
        )
    
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
    
    # If we created a new session, set the cookie
    if response_object:
        response_dict = response.model_dump()
        for key, value in response_dict.items():
            setattr(response_object, key, value)
        return response_object
    
    return response

@router.get("/history", response_model=HistoryResponse)
async def get_history(request: Request, limit: int = 5):
    # Extract session ID from cookies
    session_id = request.cookies.get("session_id")
    
    # Return empty history if no session exists instead of error
    if not session_id:
        return HistoryResponse(guesses=[])
    
    # Get history
    history = game_service.get_history(session_id, limit)
    
    return HistoryResponse(guesses=history)

@router.post("/reset")
async def reset_game(request: Request):
    # Extract session ID from cookies or create a new one
    session_id = request.cookies.get("session_id")
    
    # If no session exists, create one
    response = {"message": "Game has been reset"}
    if not session_id:
        session_id = str(uuid.uuid4())
        response_obj = Response(content=str(response))
        response_obj.set_cookie(
            key="session_id", 
            value=session_id, 
            httponly=True,
            samesite="None",
            secure=True
        )
        return response_obj
    
    # Reset the game
    game_service.reset_game(session_id)
    
    return response
