.PHONY: help install run-api run-ui run-cli test docker-build docker-run clean

help:
	@echo "Chatbot Project Commands"
	@echo "======================="
	@echo "install     - Install dependencies and setup project"
	@echo "run-api     - Start FastAPI server"
	@echo "run-ui      - Start Streamlit UI"
	@echo "run-cli     - Start CLI interface"
	@echo "test        - Run tests"
	@echo "docker-build - Build Docker image"
	@echo "docker-run  - Run Docker container"
	@echo "clean       - Clean up generated files"

install:
	python setup.py

run-api:
	uvicorn chatbot.langgraph_api:app --host 0.0.0.0 --port 8000 --reload

run-ui:
	streamlit run chatbot/app.py

run-cli:
	python chatbot/langgraph_app.py

test:
	python test_api.py

docker-build:
	docker build -t chatbot:latest .

docker-run:
	docker run -p 8000:8000 --env-file .env chatbot:latest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete