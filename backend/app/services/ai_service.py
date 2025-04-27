import google.generativeai as genai
from ..core.config import settings
from ..db.redis import redis_client

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    async def check_if_beats(self, guess, current_item):
        # Create a cache key
        cache_key = f"beats:{guess.lower()}:{current_item.lower()}"
        
        # Check if response is cached
        cached_response = await redis_client.get_cache(cache_key)
        if cached_response:
            return cached_response == "YES"
        
        # Handle traditional rock-paper-scissors rules directly
        guess_lower = guess.lower()
        current_lower = current_item.lower()
        
        # Special cases for the traditional game rules
        if guess_lower == "paper" and current_lower == "rock":
            await redis_client.set_cache(cache_key, "YES")
            return True
        elif guess_lower == "scissors" and current_lower == "paper":
            await redis_client.set_cache(cache_key, "YES")
            return True
        elif guess_lower == "rock" and current_lower == "scissors":
            await redis_client.set_cache(cache_key, "YES")
            return True
        
        # Generate prompt for Gemini - incorporate system instructions directly in the user prompt
        prompt = f"""You are a judge for the 'What Beats Rock' game. You understand basic rock-paper-scissors rules and can evaluate creative answers logically. Answer only with YES or NO.

In the game 'What Beats Rock', please determine if '{guess}' beats '{current_item}'.

Basic rules to always follow:
- Paper beats Rock (paper covers rock)
- Scissors beats Paper (scissors cut paper)
- Rock beats Scissors (rock smashes scissors)

Beyond these basic rules, evaluate creatively and logically:
- Does '{guess}' have a physical, conceptual, or logical advantage over '{current_item}'?
- Could '{guess}' destroy, alter, contain, or render '{current_item}' ineffective?

Answer only YES or NO."""
        
        try:
            # Call Gemini API - without the system role
            generation_config = {
                "temperature": 0.2,
                "max_output_tokens": 10,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            # Use a single content part with the user role
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Extract answer - get the response text
            answer = response.text.strip().upper()
            if answer not in ["YES", "NO"]:
                answer = "NO"
            
            # Cache the response
            await redis_client.set_cache(cache_key, answer)
            
            return answer == "YES"
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return False

ai_service = AIService()
