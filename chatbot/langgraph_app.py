import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

load_dotenv()

# Validate required environment variables
if not os.getenv("GROQ_API_KEY"):
    print("Error: GROQ_API_KEY environment variable is required")
    exit(1)

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
    # state["messages"] is a list of messages
    user_message = state["messages"][-1].content
    docs = retriever.invoke(user_message)
    docs_text = "".join(d.page_content for d in docs)
    # Always update the system prompt with new context
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

# Define the graph
graph = StateGraph(ChatState)
graph.add_node("bot", bot_node)
graph.set_entry_point("bot")
graph.add_edge("bot", END)
app = graph.compile()  # <-- assign compiled graph to 'app'

# Example conversation loop
if __name__ == "__main__":
    print("Welcome to the LangGraph Groq Chatbot! Type 'exit' to quit.")
    messages = [
        SystemMessage(content=system_prompt.format(context="Large Language Models (LLMs), memory, planning, and tools."))
    ]
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        messages.append(HumanMessage(content=user_input))
        state = {"messages": messages}
        state = app.invoke(state)  # <-- use 'app' instead of 'graph'
        print(f"Bot: {state['messages'][-1].content}")