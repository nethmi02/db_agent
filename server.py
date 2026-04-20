from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
from dbagent import DBAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="DBAgent Chatbot API")

# Mount a 'static' directory to serve frontend files
# We will create this directory in Phase 2
import os
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize our AI agent
try:
    agent = DBAgent()
    logger.info("DBAgent initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize DBAgent: {e}")
    agent = None

# Request model for chat endpoint
class ChatRequest(BaseModel):
    message: str

# Response model for chat endpoint
class ChatResponse(BaseModel):
    reply: str

@app.get("/")
async def serve_frontend():
    """Serve the main HTML file containing the chat UI."""
    # Ensure index.html exists before serving
    if not os.path.exists("static/index.html"):
        return {"message": "index.html not found. Please complete Phase 2 to create the UI."}
    return FileResponse("static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Handle incoming chat messages and return the agent's response."""
    if not agent:
        raise HTTPException(status_code=500, detail="DBAgent is not properly configured. Check server logs.")
    
    user_message = request.message
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    try:
        logger.info(f"Received message: {user_message}")
        # Assuming the agent has a 'chat' method representing basic usage
        reply = agent.chat(user_message)
        return ChatResponse(reply=reply)
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing your request.")

# For running locally via 'python server.py'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
