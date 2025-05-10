import os
from groq import Groq
from ..core.config import settings
from ..db.redis import redis_client

# Initialize Groq client
client = Groq(api_key="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")

class AIService:
    def __init__(self):
        self.model = "llama-3.1-8b-instant"  # e.g., "llama3-70b-8192"

    async def check_if_beats(self, guess, current_item):
        cache_key = f"beats:{guess.lower()}:{current_item.lower()}"
        
        # Check if cached
        cached_response = await redis_client.get_cache(cache_key)
        if cached_response:
            return cached_response == "YES"

        guess_lower = guess.lower()
        current_lower = current_item.lower()

        # Traditional rule short-circuit
        if guess_lower == "paper" and current_lower == "rock":
            await redis_client.set_cache(cache_key, "YES")
            return True
        elif guess_lower == "scissors" and current_lower == "paper":
            await redis_client.set_cache(cache_key, "YES")
            return True
        elif guess_lower == "rock" and current_lower == "scissors":
            await redis_client.set_cache(cache_key, "YES")
            return True

        # Prompt for Groq/LLaMA
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
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=10,
            )
            
            answer = response.choices[0].message.content.strip().upper()
            if answer not in ["YES", "NO"]:
                print(f"Unexpected response: {response.choices[0].message.content}")
                answer = "NO"

            await redis_client.set_cache(cache_key, answer)
            return answer == "YES"
        
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return False

ai_service = AIService()
