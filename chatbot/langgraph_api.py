import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

load_dotenv()

# Validate required environment variables
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is required")

system_prompt = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.
Context: {context}:"""

class DummyRetriever:
    def invoke(self, question):
        class Doc:
            def __init__(self, content):
                self.page_content = content
        return [Doc("Large Language Models (LLMs), memory, planning, and tools.")]

retriever = DummyRetriever()

def bot_node(state):
    user_message = state["messages"][-1].content
    docs = retriever.invoke(user_message)
    docs_text = "".join(d.page_content for d in docs)
    state["messages"][0] = SystemMessage(content=system_prompt.format(context=docs_text))
    model = ChatGroq(
        model="llama3-70b-8192",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    response = model.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    return state

class ChatState(TypedDict):
    messages: List[BaseMessage]

graph = StateGraph(ChatState)
graph.add_node("bot", bot_node)
graph.set_entry_point("bot")
graph.add_edge("bot", END)
app_graph = graph.compile()

# FastAPI app
app = FastAPI(title="Chatbot API", version="1.0.0")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

class Message(BaseModel):
    type: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        # Convert incoming messages to LangChain message objects
        lc_messages = []
        for msg in request.messages:
            if msg["type"] == "human":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["type"] == "ai":
                lc_messages.append(AIMessage(content=msg["content"]))
            elif msg["type"] == "system":
                lc_messages.append(SystemMessage(content=msg["content"]))
        
        if not lc_messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        state = {"messages": lc_messages}
        state = app_graph.invoke(state)
        return {"response": state["messages"][-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")