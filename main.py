"""
Quantum Risk Analyzer - Entry Point

Run this script to start the Streamlit application:
    python main.py

Or use the streamlit command directly:
    streamlit run app.py
"""

import subprocess
import sys
import os


def main():
    """Start the Streamlit application"""

    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")

    print("=" * 60)
    print("  Quantum Risk Analyzer v2.0")
    print("  Enterprise Cryptographic Assessment Platform")
    print("=" * 60)
    print()
    print("Starting Streamlit application...")
    print()
    print("The app will open in your default browser.")
    print("Press Ctrl+C to stop the server.")
    print()

    # Run streamlit
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", app_path],
            cwd=script_dir
        )
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        print("Thanks for using Quantum Risk Analyzer!")
    except Exception as e:
        print(f"Error starting application: {e}")
        print("\nTry running directly with:")
        print("    streamlit run app.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
