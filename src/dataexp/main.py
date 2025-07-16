#!/usr/bin/env python
import sys
import warnings
import os
from pathlib import Path

from datetime import datetime

from dataexp.crew import Dataexp

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Use OS-generic path handling
    data_file = Path(__file__).parent / 'data' / 'titanic.csv'
    
    # Debug: Print the resolved path
    print(f"Looking for data file at: {data_file}")
    print(f"File exists: {data_file.exists()}")

    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    inputs = {
        'filename': str(data_file),  # Convert Path to string
        'user_request': 'What is the average age of passengers in the Titanic dataset?',
    }
    
    try:
        Dataexp().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    # Use OS-generic path handling
    data_file = Path(__file__).parent / 'data' / 'titanic.csv'
    
    inputs = {
        'filename': str(data_file),  # Convert Path to string
        'user_request': 'What is the average age of passengers in the Titanic dataset?',
    }
    try:
        Dataexp().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Dataexp().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    # Use OS-generic path handling
    data_file = Path(__file__).parent / 'data' / 'titanic.csv'
    
    inputs = {
        'filename': str(data_file),  # Convert Path to string
        'user_request': 'What is the average age of passengers in the Titanic dataset?',
    }
    
    try:
        Dataexp().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_streamlit():
    """
    Run the Streamlit web interface.
    """
    import subprocess
    import sys
    from pathlib import Path
    
    app_path = Path(__file__).parent.parent.parent / "app.py"
    
    try:
        print("🚀 Starting Streamlit app...")
        print(f"📁 App location: {app_path}")
        print("🌐 Opening in browser at: http://localhost:8501")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n✅ Streamlit app stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
