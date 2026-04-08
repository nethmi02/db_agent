from sqlalchemy import create_engine, inspect
from dbagent.config import DATABASE_URL

class SchemaTool:
    """Tool that automatically inspects your database and extracts its structure."""
    
    def __init__(self, db_url: str = DATABASE_URL):
        self.engine = create_engine(db_url)

    def get_schema(self) -> str:
        """
        Reads all tables and columns from the database, creating a cheat sheet
        for the AI to know what data it can query.
        
        Returns:
            A formatted string describing the database schema.
        """
        inspector = inspect(self.engine)
        schema_text = "Database Schema:\n"
        
        # Go through each table in the database
        for table_name in inspector.get_table_names():
            schema_text += f"\nTable: {table_name}\n"
            schema_text += "Columns:\n"
            
            # Go through each column in the table
            for column in inspector.get_columns(table_name):
                col_name = column['name']
                col_type = str(column['type'])
                schema_text += f" - {col_name} ({col_type})\n"
                
        return schema_text
