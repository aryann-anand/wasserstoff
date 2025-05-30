from ..utils.linked_list import LinkedList
from ..db.mongodb import mongodb
from .ai_service import ai_service
from .moderation_service import moderation_service
from ..core.config import settings
import uuid

class GameService:
    def __init__(self):
        self.games = {}
    
    def create_game(self, session_id=None):
        if not session_id:
            session_id = str(uuid.uuid4())
        
        game = {
            "guesses": LinkedList(),
            "current_item": settings.STARTING_WORD,
            "score": 0,
            "game_over": False
        }
        
        # Add the starting word to the linked list
        game["guesses"].append(settings.STARTING_WORD)
        
        self.games[session_id] = game
        return session_id
    
    def get_game(self, session_id):
        return self.games.get(session_id)
    
    def reset_game(self, session_id):
        if session_id in self.games:
            self.games[session_id] = {
                "guesses": LinkedList(),
                "current_item": settings.STARTING_WORD,
                "score": 0,
                "game_over": False
            }
            # Add the starting word to the linked list
            self.games[session_id]["guesses"].append(settings.STARTING_WORD)
        return session_id
    
    async def process_guess(self, session_id, guess, persona="cheery"):
        # Get the game state
        game = self.get_game(session_id)
        if not game:
            session_id = self.create_game(session_id)
            game = self.get_game(session_id)
        
        # If game is over, return
        if game["game_over"]:
            return {
                "success": False,
                "message": "Game is already over. Please reset to play again.",
                "last_guess": guess,
                "previous_item": game["current_item"],
                "score": game["score"],
                "global_count": 0,
                "game_over": True
            }
        
        # Check if the guess contains profanity
        if moderation_service.check_content(guess):
            return {
                "success": False,
                "message": "Please avoid using inappropriate language.",
                "last_guess": moderation_service.censor_content(guess),
                "previous_item": game["current_item"],
                "score": game["score"],
                "global_count": 0,
                "game_over": False
            }
        
        # Check if the guess already exists in the linked list
        if game["guesses"].contains(guess):
            game["game_over"] = True
            message = settings.PERSONAS[persona]["duplicate_response"].format(guess, game["score"])
            return {
                "success": False,
                "message": message,
                "last_guess": guess,
                "previous_item": game["current_item"],
                "score": game["score"],
                "global_count": 0,
                "game_over": True
            }
        
        # Check if the guess beats the current item using AI
        beats = await ai_service.check_if_beats(guess, game["current_item"])
        
        # Get the global count
        db = mongodb.get_db()
        guess_stat = await db.guess_stats.find_one({"guess": guess})
        guess_count = 0
        
        if beats:
        # Increment the global count
            if guess_stat:
                guess_count = guess_stat["count"] + 1
                await db.guess_stats.update_one(
                    {"guess": guess},
                    {"$inc": {"count": 1}}
                )
            else:
                guess_count = 1
                await db.guess_stats.insert_one({
                    "guess": guess,
                    "count": 1
                })
            
            # Update the game state
            game["score"] += 1
            old_current_item = game["current_item"]  # Store the old value before updating
            game["current_item"] = guess
            game["guesses"].append(guess)
            
            message = settings.PERSONAS[persona]["positive_response"].format(guess, old_current_item, guess_count)
            
            return {
                "success": True,
                "message": message,
                "last_guess": guess,
                "previous_item": old_current_item,  # Use old value here
                "score": game["score"],
                "global_count": guess_count,
                "game_over": False
            }

        else:
            # End the game
            game["game_over"] = True
            message = settings.PERSONAS[persona]["negative_response"].format(guess, game["current_item"], game["score"])
            
            return {
                "success": False,
                "message": message,
                "last_guess": guess,
                "previous_item": game["current_item"],
                "score": game["score"],
                "global_count": guess_count,
                "game_over": True
            }
    
    def get_history(self, session_id, limit=5):
        game = self.get_game(session_id)
        if not game:
            return []
        
        return game["guesses"].get_last_n(limit)

game_service = GameService()
