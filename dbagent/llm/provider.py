import os
from groq import Groq
from dbagent.config import LLM_MODEL, GROQ_API_KEY, validate_config

class LLMProvider:
    """Wrapper around Groq API to send prompts and get responses using LLaMA models."""
    
    def __init__(self):
        # Make sure our config is valid before trying to use the LLM
        validate_config()
        
        # Initialize the Groq client
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = self._get_best_model()

    def _get_best_model(self) -> str:
        """Automatically find an active model if the current one is decommissioned."""
        try:
            # 1. Ask Groq for the list of all currently active models
            active_models = [m.id for m in self.client.models.list().data]
            
            # 2. If the model from our .env file is still active, just use it
            if LLM_MODEL != "auto" and LLM_MODEL in active_models:
                return LLM_MODEL
                
            print(f"\n⚠️ Model '{LLM_MODEL}' not found or set to auto. Auto-selecting the best available model...")
            
            # 3. Otherwise, search the active list for the smartest Llama 70B model 
            llama_70b_models = [m for m in active_models if "70b" in m.lower() and "llama" in m.lower()]
            if llama_70b_models:
                llama_70b_models.sort(reverse=True) # Sort so 3.3 comes before 3.1
                print(f"✅ Auto-selected model: {llama_70b_models[0]}\n")
                return llama_70b_models[0]
                
            # 4. Ultimate fallback: just grab the first Llama model they have
            llama_models = [m for m in active_models if "llama" in m.lower()]
            return llama_models[0] if llama_models else active_models[0]
        except Exception as e:
            print(f"Could not auto-fetch models: {e}")
            # Fallback to a relatively safe modern default
            return "llama-3.3-70b-versatile"
        
    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to the LLM and returns the text response.
        
        Args:
            prompt: The full text prompt (instructions + conversation + schema)
            
        Returns:
            The text response from the LLM.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"
