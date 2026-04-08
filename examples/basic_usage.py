import os
from dbagent import DBAgent

def run_demo():
    print("🚀 Initializing DBAgent...")
    
    # Notice we don't even specify the database URL or API key here!
    # It automatically loads them from your .env file
    agent = DBAgent()
    
    print("\n---------------------------------------------------------")
    print(" 🤖 DBAgent is ready. Ask it a question about your data!")
    print("---------------------------------------------------------")
    
    while True:
        try:
            user_input = input("\n👤 You: ")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                break
                
            print("\n🔄 Processing...")
            answer = agent.chat(user_input)
            
            print("\n💬 Final Answer:")
            print(answer)
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            break
        except Exception as e:
            print(f"\n❌ Oops! An error occurred: {e}")

if __name__ == "__main__":
    run_demo()
