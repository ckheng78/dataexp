#!/usr/bin/env python
"""
Launcher script for the Streamlit app
"""
import subprocess
import sys
from pathlib import Path

def run_streamlit():
    """Run the Streamlit app"""
    app_path = Path(__file__).parent / "app.py"
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\nStreamlit app stopped.")
    except Exception as e:
        print(f"Error running Streamlit: {e}")

if __name__ == "__main__":
    run_streamlit()
