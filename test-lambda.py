#!/usr/bin/env python3
"""Test Lambda deployment locally"""
import json
from lambda_handler import handler

def test_lambda():
    # Test health endpoint
    event = {
        "httpMethod": "GET",
        "path": "/health",
        "headers": {},
        "body": None
    }
    
    response = handler(event, {})
    print("Health Check Response:", response)
    
    # Test chat endpoint
    chat_event = {
        "httpMethod": "POST",
        "path": "/chat",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "messages": [{"type": "human", "content": "Hello"}]
        })
    }
    
    response = handler(chat_event, {})
    print("Chat Response:", response)

if __name__ == "__main__":
    test_lambda()