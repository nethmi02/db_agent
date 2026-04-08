from dbagent.config import MEMORY_LIMIT

class ConversationMemory:
    """Stores the conversation history so the agent understands context."""
    
    def __init__(self, limit: int = MEMORY_LIMIT):
        self.messages = []
        self.limit = limit
        
    def add_user_message(self, text: str):
        self.messages.append({"role": "user", "content": text})
        self._enforce_limit()
        
    def add_assistant_message(self, text: str):
        self.messages.append({"role": "assistant", "content": text})
        self._enforce_limit()
        
    def get_history_text(self) -> str:
        """Formats the history into a prompt-friendly string."""
        if not self.messages:
            return "No previous conversation."
            
        history = "Previous Conversation:\n"
        for msg in self.messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            history += f"{role}: {msg['content']}\n"
            
        return history
        
    def _enforce_limit(self):
        """Ensures the memory doesn't get too large (saves tokens and money)."""
        # A message pair is (user + assistant), so limit * 2 is max raw length.
        # This keeps the last X interactions.
        if len(self.messages) > self.limit * 2:
            # remove the oldest conversation pair
            self.messages = self.messages[-self.limit * 2:]
