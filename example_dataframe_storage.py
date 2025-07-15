#!/usr/bin/env python
"""
Example demonstrating how to store and retrieve DataFrames in CrewAI
"""
import json
from pathlib import Path
from dataexp.tools.data_tool import (
    execute_sql_on_csv, 
    save_dataframe, 
    load_dataframe,
    cache_dataframe,
    get_cached_dataframe
)

def demonstrate_dataframe_storage():
    """
    Demonstrate different ways to store DataFrames in CrewAI
    """
    # Sample data file path
    data_file = Path(__file__).parent / "src" / "dataexp" / "data" / "titanic.csv"
    
    print("=== DataFrame Storage Methods in CrewAI ===\n")
    
    # 1. Execute SQL and get results
    print("1. Execute SQL Query:")
    sql_query = "SELECT Pclass, AVG(Age) as avg_age FROM df WHERE Age IS NOT NULL GROUP BY Pclass ORDER BY Pclass"
    result = execute_sql_on_csv(str(data_file), sql_query)
    print(f"Query Result: {result[:200]}...\n")
    
    # 2. Save DataFrame to file (CSV)
    print("2. Save DataFrame to CSV:")
    save_result = save_dataframe(result, "titanic_avg_age_by_class", "csv")
    print(f"Save Result: {save_result}\n")
    
    # 3. Save DataFrame to JSON
    print("3. Save DataFrame to JSON:")
    save_result = save_dataframe(result, "titanic_avg_age_by_class", "json")
    print(f"Save Result: {save_result}\n")
    
    # 4. Cache DataFrame in memory
    print("4. Cache DataFrame in memory:")
    cache_result = cache_dataframe(result, "avg_age_by_class")
    print(f"Cache Result: {cache_result}\n")
    
    # 5. Retrieve cached DataFrame
    print("5. Retrieve cached DataFrame:")
    cached_data = get_cached_dataframe("avg_age_by_class")
    print(f"Cached Data: {cached_data[:200]}...\n")
    
    # 6. Load DataFrame from saved file
    print("6. Load DataFrame from saved file:")
    loaded_data = load_dataframe("output/titanic_avg_age_by_class.csv")
    print(f"Loaded Data: {loaded_data[:200]}...\n")
    
    print("=== Summary ===")
    print("CrewAI supports multiple DataFrame storage methods:")
    print("1. Task output files (automatic)")
    print("2. Manual file saving (CSV, JSON, Parquet, Pickle)")
    print("3. In-memory caching (temporary)")
    print("4. File loading (persistent)")

if __name__ == "__main__":
    demonstrate_dataframe_storage()
