#!/usr/bin/env python3
"""
Simple test script for the chatbot API
"""
import requests
import json

def test_api():
    """Test the chatbot API endpoint"""
    url = "http://localhost:8000/chat"
    
    test_message = {
        "messages": [
            {"type": "human", "content": "What are LLMs?"}
        ]
    }
    
    try:
        response = requests.post(url, json=test_message)
        if response.status_code == 200:
            result = response.json()
            print("✅ API Test Successful!")
            print(f"Response: {result['response']}")
        else:
            print(f"❌ API Test Failed: {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running")
        print("Start with: uvicorn chatbot.langgraph_api:app --host 0.0.0.0 --port 8000")

def test_health():
    """Test the health endpoint"""
    url = "http://localhost:8000/health"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Health Check Passed!")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running")

if __name__ == "__main__":
    print("Testing Chatbot API...")
    test_health()
    test_api()