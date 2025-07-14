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
