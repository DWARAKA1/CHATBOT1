#!/usr/bin/env python3
"""
Setup script for the chatbot project
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_project():
    """Set up the project environment"""
    print("🚀 Setting up Chatbot Project")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("⚠️  .env file not found")
        print("📝 Creating .env from template...")
        with open(".env.example", "r") as src, open(".env", "w") as dst:
            dst.write(src.read())
        print("✅ .env file created. Please edit it with your GROQ_API_KEY")
    else:
        print("✅ .env file exists")
    
    # Test imports
    try:
        from chatbot.langgraph_api import app
        print("✅ FastAPI app import successful")
    except ImportError as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False
    
    try:
        from chatbot.langgraph_app import app
        print("✅ LangGraph app import successful")
    except ImportError as e:
        print(f"❌ LangGraph app import failed: {e}")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your GROQ_API_KEY")
    print("2. Run FastAPI server: uvicorn chatbot.langgraph_api:app --host 0.0.0.0 --port 8000")
    print("3. Or run Streamlit UI: streamlit run chatbot/app.py")
    print("4. Or run CLI interface: python chatbot/langgraph_app.py")
    
    return True

if __name__ == "__main__":
    success = setup_project()
    sys.exit(0 if success else 1)