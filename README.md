# Chatbot with LangGraph and Groq

A conversational AI chatbot built with LangGraph, Groq LLM, and FastAPI/Streamlit interfaces.

## Features

- **FastAPI REST API**: HTTP endpoint for chat interactions
- **Streamlit Web UI**: Interactive web interface
- **LangGraph Integration**: Structured conversation flow
- **Groq LLM**: Fast inference with Llama 3 70B model
- **Docker Support**: Containerized deployment

## Setup

### Prerequisites

- Python 3.11+
- Groq API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd chatbot1
```

2. Run setup script:
```bash
python setup.py
```

3. Edit `.env` file with your Groq API key:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

Alternatively, use Make commands:
```bash
make install
```

### Running the Application

#### FastAPI Server
```bash
uvicorn chatbot.langgraph_api:app --host 0.0.0.0 --port 8000
# Or use: make run-api
```

#### Streamlit UI
```bash
streamlit run chatbot/app.py
# Or use: make run-ui
```

#### Command Line Interface
```bash
python chatbot/langgraph_app.py
# Or use: make run-cli
```

### Docker Deployment

```bash
docker build -t chatbot .
docker run -p 8000:8000 --env-file .env chatbot
# Or use: make docker-build && make docker-run
```

### Testing

```bash
python test_api.py
# Or use: make test
```

## API Usage

### POST /chat

```json
{
  "messages": [
    {"type": "human", "content": "What are LLMs?"}
  ]
}
```

Response:
```json
{
  "response": "Large Language Models (LLMs) are AI systems trained on vast amounts of text data..."
}
```

## Project Structure

```
chatbot1/
├── chatbot/
│   ├── app.py              # Streamlit UI
│   ├── langgraph_api.py    # FastAPI server
│   └── langgraph_app.py    # CLI interface
├── requirements.txt        # Dependencies
├── Dockerfile             # Container config
├── .env.example          # Environment template
└── README.md             # This file
```

## License

MIT License