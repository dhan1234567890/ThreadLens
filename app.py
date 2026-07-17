import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Cyber Threat Assistant", page_icon="🛡️", layout="wide")

st.title("🛡️ LLM-Powered Network Threat Assistant")
st.markdown("""
This assistant uses **Graph RAG (Neo4j)** and **Large Language Models** to analyze your cybersecurity data.
You can ask questions about your network traffic, firewall logs, and IDS alerts.
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about potential threats (e.g., 'Explain the SQL Injection attempt alert')"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Backend API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analyzing graph data...")
        
        try:
            response = requests.post(f"{API_URL}/query", json={"query": prompt})
            response.raise_for_status()
            
            answer = response.json().get("response", "No response received.")
            message_placeholder.markdown(answer)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to connect to the backend API: {e}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
