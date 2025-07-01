import json
from mangum import Mangum
from chatbot.langgraph_api import app

# Lambda handler
handler = Mangum(app)