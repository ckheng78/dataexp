import pandas as pd
import numpy as np
import json
from crewai.tools import tool
from pandasql import sqldf

@tool("Extract the column names from a CSV file")
def get_column_names(filename: str) -> str:
    """
    Extract the column names from a CSV file.

    Args:
        filename: The name of the file to read (e.g., CSV file)

    Returns:
        String representation of the column names in JSON format.
    """
    try:
        df = pd.read_csv(filename)
        
        # Include column names and their data types
        columns_with_types = {
            "columns": [
                {"name": col, "dtype": str(df[col].dtype)} 
                for col in df.columns
            ]
        }
        return json.dumps(columns_with_types)
    except Exception as e:
        return f"Error creating DataFrame: {str(e)}"


@tool("Execute SQL query on CSV file")
def execute_sql_on_csv(filename: str, sql_query: str) -> str:
    """
    Read a CSV file into a pandas DataFrame and execute a SQL query on it.
    
    Args:
        filename: The path to the CSV file to read
        sql_query: The SQL statement to execute on the DataFrame
        
    Returns:
        JSON string representation of the query results
    """
    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(filename)
        
        # Execute SQL query using pandasql
        # pandasql uses SQLite syntax and can query pandas DataFrames
        result = sqldf(sql_query, locals())
        
        # Convert result to JSON
        if result is not None and not result.empty:
            return result.to_json(orient='records', date_format='iso')
        else:
            return json.dumps({"message": "Query executed successfully but returned no results"})
            
    except FileNotFoundError:
        return json.dumps({"error": f"File not found: {filename}"})
    except Exception as e:
        return json.dumps({"error": f"Error executing SQL query: {str(e)}"})


@tool("Get DataFrame info and sample data")
def get_dataframe_info(filename: str, sample_rows: int = 5) -> str:
    """
    Get basic information about a CSV file including column info and sample data.
    
    Args:
        filename: The path to the CSV file to analyze
        sample_rows: Number of sample rows to include (default: 5)
        
    Returns:
        JSON string with DataFrame info and sample data
    """
    try:
        df = pd.read_csv(filename)
        
        # Get basic info
        info = {
            "shape": df.shape,
            "columns": [{"name": col, "dtype": str(df[col].dtype)} for col in df.columns],
            "null_counts": df.isnull().sum().to_dict(),
            "sample_data": df.head(sample_rows).to_dict(orient='records')
        }
        
        return json.dumps(info, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error analyzing DataFrame: {str(e)}"})

