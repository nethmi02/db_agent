from sqlalchemy import create_engine, text
from dbagent.config import DATABASE_URL

class DBTool:
    """A safe wrapper around our database to run SQL queries."""
    
    def __init__(self, db_url: str = DATABASE_URL):
        # Create an engine that connects to our database
        self.engine = create_engine(db_url)
        
    def run_query(self, query: str) -> list[dict]:
        """
        Executes a SELECT query and returns the results.
        
        Args:
            query: The SQL string to run
            
        Returns:
            A list of rows, where each row is a dictionary.
        """
        # --- Safety Check Here ---
        # The AI should ONLY run SELECT queries. No DELETING, DROPPING, or UPDATING!
        clean_query = query.strip().upper()
        if not clean_query.startswith("SELECT"):
            return [{"error": "Tool rejected query! Only SELECT queries are permitted."}]
        
        try:
            with self.engine.connect() as conn:
                # Run the query
                result = conn.execute(text(query))
                
                # Convert the raw database rows into Python dictionaries
                rows = []
                for row in result.mappings():
                    # converting to standard python dictionary
                    rows.append(dict(row))
                    
                return rows
        except Exception as e:
            # If the AI wrote bad SQL, it will get the error message back to learn from
            return [{"error": f"SQL Error: {str(e)}"}]
