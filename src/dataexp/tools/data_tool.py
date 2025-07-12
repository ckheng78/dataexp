import pandas as pd
import numpy as np
from crewai.tools import tool

@tool
def create_dataframe_from_data(data: str) -> str:
    """
    Creates a pandas DataFrame from string data.
    
    Args:
        data: String representation of data (e.g., CSV format)
    
    Returns:
        String representation of the DataFrame
    """
    try:
        # Convert string data to DataFrame
        from io import StringIO
        df = pd.read_csv(StringIO(data))
        return df.to_string()
    except Exception as e:
        return f"Error creating DataFrame: {str(e)}"

@tool
def analyze_data(data: str) -> str:
    """
    Analyzes data and provides basic statistics.
    
    Args:
        data: String representation of data
    
    Returns:
        String with data analysis results
    """
    try:
        from io import StringIO
        df = pd.read_csv(StringIO(data))
        
        analysis = f"""
        Data Analysis Results:
        - Shape: {df.shape}
        - Columns: {list(df.columns)}
        - Data Types: {df.dtypes.to_dict()}
        - Missing Values: {df.isnull().sum().to_dict()}
        - Basic Statistics:
        {df.describe().to_string()}
        """
        return analysis
    except Exception as e:
        return f"Error analyzing data: {str(e)}"
