"""
Main entry point for the Agentic RAG system.
This file serves as an alternative entry point to app.py.
"""

if __name__ == "__main__":
    # Import and run the main application
    from app import main
    import sys
    
    exit_code = main()
    sys.exit(exit_code)