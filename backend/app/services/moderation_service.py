from better_profanity import profanity

class ModerationService:
    def __init__(self):
        profanity.load_censor_words()
    
    def check_content(self, text):
        return profanity.contains_profanity(text)
    
    def censor_content(self, text):
        return profanity.censor(text)

moderation_service = ModerationService()
