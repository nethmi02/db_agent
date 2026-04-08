import google.generativeai as genai
from dbagent.config import LLM_MODEL, GEMINI_API_KEY, validate_config

class LLMProvider:
    """Wrapper around Google Gemini API to send prompts and get responses."""
    
    def __init__(self):
        # Make sure our config is valid before trying to use the LLM
        validate_config()
        
        # Configure the Gemini API with our key
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialize the model (e.g., gemini)
        self.model = genai.GenerativeModel(LLM_MODEL)
        
    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to the LLM and returns the text response.
        
        Args:
            prompt: The full text prompt (instructions + conversation + schema)
            
        Returns:
            The text response from the LLM.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"
