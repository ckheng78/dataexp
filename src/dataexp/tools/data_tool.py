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

@tool("Save DataFrame to file")
def save_dataframe(data: str, filename: str, format: str = "csv") -> str:
    """
    Save a DataFrame (from JSON string) to a file in various formats.
    
    Args:
        data: JSON string representation of the DataFrame
        filename: The output filename (without extension)
        format: Output format ('csv', 'json', 'parquet', 'pickle')
        
    Returns:
        JSON string with save status and file path
    """
    try:
        import json
        from pathlib import Path
        
        # Parse JSON data back to DataFrame
        data_dict = json.loads(data)
        df = pd.DataFrame(data_dict)
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Save based on format
        if format.lower() == "csv":
            file_path = output_dir / f"{filename}.csv"
            df.to_csv(file_path, index=False)
        elif format.lower() == "json":
            file_path = output_dir / f"{filename}.json"
            df.to_json(file_path, orient='records', indent=2)
        elif format.lower() == "parquet":
            file_path = output_dir / f"{filename}.parquet"
            df.to_parquet(file_path, index=False)
        elif format.lower() == "pickle":
            file_path = output_dir / f"{filename}.pkl"
            df.to_pickle(file_path)
        else:
            return json.dumps({"error": f"Unsupported format: {format}"})
        
        return json.dumps({
            "status": "success",
            "file_path": str(file_path),
            "format": format,
            "rows": len(df),
            "columns": len(df.columns)
        })
        
    except Exception as e:
        return json.dumps({"error": f"Error saving DataFrame: {str(e)}"})


@tool("Load DataFrame from file")
def load_dataframe(filename: str) -> str:
    """
    Load a DataFrame from a file and return as JSON string.
    
    Args:
        filename: The file path to load from
        
    Returns:
        JSON string representation of the DataFrame
    """
    try:
        from pathlib import Path
        
        file_path = Path(filename)
        
        if not file_path.exists():
            return json.dumps({"error": f"File not found: {filename}"})
        
        # Load based on file extension
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() == ".json":
            df = pd.read_json(file_path)
        elif file_path.suffix.lower() == ".parquet":
            df = pd.read_parquet(file_path)
        elif file_path.suffix.lower() == ".pkl":
            df = pd.read_pickle(file_path)
        else:
            return json.dumps({"error": f"Unsupported file format: {file_path.suffix}"})
        
        return df.to_json(orient='records')
        
    except Exception as e:
        return json.dumps({"error": f"Error loading DataFrame: {str(e)}"})


@tool("Create DataFrame cache")
def cache_dataframe(data: str, cache_key: str) -> str:
    """
    Cache a DataFrame in memory for later retrieval within the same session.
    
    Args:
        data: JSON string representation of the DataFrame
        cache_key: Unique key to identify the cached DataFrame
        
    Returns:
        JSON string with cache status
    """
    try:
        import json
        
        # Initialize cache if it doesn't exist
        if not hasattr(cache_dataframe, '_cache'):
            cache_dataframe._cache = {}
        
        # Parse and cache the data
        data_dict = json.loads(data)
        df = pd.DataFrame(data_dict)
        cache_dataframe._cache[cache_key] = df
        
        return json.dumps({
            "status": "cached",
            "cache_key": cache_key,
            "rows": len(df),
            "columns": len(df.columns),
            "cached_items": len(cache_dataframe._cache)
        })
        
    except Exception as e:
        return json.dumps({"error": f"Error caching DataFrame: {str(e)}"})


@tool("Retrieve cached DataFrame")
def get_cached_dataframe(cache_key: str) -> str:
    """
    Retrieve a cached DataFrame.
    
    Args:
        cache_key: The key used to cache the DataFrame
        
    Returns:
        JSON string representation of the cached DataFrame
    """
    try:
        if not hasattr(cache_dataframe, '_cache'):
            return json.dumps({"error": "No cache initialized"})
        
        if cache_key not in cache_dataframe._cache:
            available_keys = list(cache_dataframe._cache.keys())
            return json.dumps({
                "error": f"Cache key '{cache_key}' not found",
                "available_keys": available_keys
            })
        
        df = cache_dataframe._cache[cache_key]
        return df.to_json(orient='records')
        
    except Exception as e:
        return json.dumps({"error": f"Error retrieving cached DataFrame: {str(e)}"})

