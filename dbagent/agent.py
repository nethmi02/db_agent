import re
from dbagent.llm.provider import LLMProvider
from dbagent.tools.schema_tool import SchemaTool
from dbagent.tools.db_tool import DBTool
from dbagent.memory.conversation import ConversationMemory
from dbagent.utils.formatter import format_data

class DBAgent:
    """
    The Brain of the operation.
    Orchestrates the LLM, the Memory, and the Database Tools.
    """
    
    def __init__(self, database_url: str = None, api_key: str = None):
        # We can pass custom values, otherwise it uses the .env fallback
        # Wait, the config module handles defaults.
        self.llm = LLMProvider()
        
        # Initialize Tools
        self.schema_tool = SchemaTool(db_url=database_url) if database_url else SchemaTool()
        self.db_tool = DBTool(db_url=database_url) if database_url else DBTool()
        
        # Initialize Memory
        self.memory = ConversationMemory()
        
        # Fetch the database structure once when starting
        self.schema = self.schema_tool.get_schema()

    def chat(self, user_prompt: str) -> str:
        """
        Main entry point for the user.
        Takes a plain English question and returns a plain English answer.
        """
        print(f"🤖 Agent thinking about: '{user_prompt}'")
        
        # 1. Ask the LLM to write the SQL query
        sql = self._generate_sql(user_prompt)
        
        # 2. Run the SQL on the real database
        print(f"🔧 Running SQL: {sql}")
        raw_results = self.db_tool.run_query(sql)
        
        # 3. Format the raw database dicts into a readable table
        formatted_results = format_data(raw_results)
        print(f"📊 Extracted data:\n{formatted_results}")
        
        # 4. Ask the LLM to explain the results back to the user
        final_answer = self._generate_final_answer(user_prompt, sql, formatted_results)
        
        # 5. Store conversation in memory for context
        self.memory.add_user_message(user_prompt)
        self.memory.add_assistant_message(final_answer)
        
        return final_answer

    def _generate_sql(self, user_prompt: str) -> str:
        """Internal step: Prompt the LLM to write pure SQL based on the schema."""
        
        prompt = f"""
You are a Database Expert AI. Your only job is to write safe, working SQL queries.
Only output the raw SQL query, DO NOT add markdown like ```sql.

{self.schema}

{self.memory.get_history_text()}

User's new request: {user_prompt}

Please write the SQL SELECT query to answer the user's request.
"""
        # Call LLM
        response = self.llm.generate(prompt)
        
        # Sometimes LLMs still add markdown, so we aggressively clean it:
        clean_sql = response.replace("```sql", "").replace("```", "").strip()
        return clean_sql

    def _generate_final_answer(self, user_prompt: str, sql: str, results_text: str) -> str:
        """Internal step: Prompt the LLM to turn raw table data into a nice human answer."""
        
        prompt = f"""
You are a helpful and polite data assistant.
The user asked: "{user_prompt}"

To answer this, I ran this SQL: {sql}

Here are the results I got back from the database:
{results_text}

Analyze the data and answer the user's question clearly in plain English.
Be direct. Do not show the SQL. Just give them the final answer.
"""
        return self.llm.generate(prompt)
