import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Validate required environment variables
if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY environment variable is required")
    st.stop()

# System prompt template
system_prompt = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.
Context: {context}:"""

# Dummy retriever for demonstration
class DummyRetriever:
    def invoke(self, question):
        class Doc:
            def __init__(self, content):
                self.page_content = content
        return [Doc("Large Language Models (LLMs), memory, planning, and tools.")]

retriever = DummyRetriever()

# Streamlit UI
st.title("Groq LLM Conversational Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=system_prompt.format(context="Large Language Models (LLMs), memory, planning, and tools."))
    ]

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system prompt
    if isinstance(msg, HumanMessage):
        st.markdown(f"**You:** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.markdown(f"**Bot:** {msg.content}")

# User input
user_input = st.text_input("Type your message:", key="input")

if st.button("Send") and user_input.strip():
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Retrieve context (dummy for now)
    docs = retriever.invoke(user_input)
    docs_text = "".join(d.page_content for d in docs)
    # Update system prompt with new context
    st.session_state.messages[0] = SystemMessage(content=system_prompt.format(context=docs_text))

    # Create Groq model
    model = ChatGroq(
        model="llama3-70b-8192",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    with st.spinner("Thinking..."):
        # Get response from model
        response = model.invoke(st.session_state.messages)
        # Add bot response to chat history
        st.session_state.messages.append(AIMessage(content=response.content))
        st.rerun()  # Refresh to show new message