#!/usr/bin/env python3
"""
Chatbot Project Entry Point

This module provides a simple entry point for the chatbot project.
For actual functionality, use the modules in the chatbot/ directory.
"""

def main():
    print("Chatbot Project")
    print("===============")
    print("")
    print("Available interfaces:")
    print("1. FastAPI Server: uvicorn chatbot.langgraph_api:app --host 0.0.0.0 --port 8000")
    print("2. Streamlit UI: streamlit run chatbot/app.py")
    print("3. CLI Interface: python chatbot/langgraph_app.py")
    print("")
    print("Make sure to set GROQ_API_KEY in your .env file")

if __name__ == "__main__":
    main()
