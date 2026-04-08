from tabulate import tabulate

def format_data(rows: list[dict]) -> str:
    """
    Takes raw dictionary rows from the database tool and turns them 
    into a pretty text table that the LLM can easily read.
    
    Example:
    From: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    To:   |   id | name  |
          |------|-------|
          |    1 | Alice |
          |    2 | Bob   |
    """
    if not rows:
        return "No data found."
        
    # Check if the query returned an error dict instead of real rows
    if isinstance(rows, list) and len(rows) > 0 and "error" in rows[0]:
        return f"Query Failed: {rows[0]['error']}"
        
    try:
        # Use tabulate to draw an ASCII table
        return tabulate(rows, headers="keys", tablefmt="pipe")
    except Exception as e:
        return f"Could not format data: {str(e)}"
