import pandas as pd
import numpy as np
from crewai.tools import tool

@tool("Create a JSON object from the filename provided")
def create_json_from_data(filename: str) -> str:
    """
    Creates a JSON object from filename provided

    Args:
        filename: The name of the file to read (e.g., CSV file)

    Returns:
        String representation of the JSON object
    """
    try:
        df = (
            pd
            .read_csv(filename)
            .pipe(lambda x: (print(x.head), x)[1])
        )
        return df.to_json()
    except Exception as e:
        return f"Error creating DataFrame: {str(e)}"

