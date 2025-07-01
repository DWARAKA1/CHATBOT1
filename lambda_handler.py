import json
import os
from mangum import Mangum
from chatbot.langgraph_api import app

# Ensure environment variables are loaded
if not os.getenv("GROQ_API_KEY"):
    print("Warning: GROQ_API_KEY not found in environment")

# Lambda handler
handler = Mangum(app, lifespan="off")