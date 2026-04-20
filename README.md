Step 1: User calls agent.chat("How many users signed up last month?")

Step 2: Agent fetches DB schema using schema_tool
        → "Table 'users': id, name, email, created_at"

Step 3: Agent sends this to LLM with a prompt:
        "You are a helpful DB assistant.
         The database has these tables: [schema]
         The user asked: 'How many users signed up last month?'
         Write a safe SQL SELECT query to answer this."

Step 4: LLM returns:
        SELECT COUNT(*) as count FROM users
        WHERE created_at >= DATE_TRUNC('month', NOW() - INTERVAL '1 month')

Step 5: Agent runs this SQL using db_tool
        → Result: [{"count": 142}]

Step 6: Agent sends results back to LLM:
        "The query returned: [{'count': 142}]
         Explain this to the user in plain English."

Step 7: LLM returns:
        "Last month, 142 new users signed up on your platform!"

Step 8: Agent adds this to memory and returns the answer to the user


this is testing line