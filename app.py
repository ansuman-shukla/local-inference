'''
This script creates a Streamlit web application for interacting with a local LLM 
via Ollama and the langchain-ollama library.

To run this script:
1. Ensure Ollama is installed and running.
2. Pull the desired model, e.g., `ollama pull phi3.5:latest`.
3. Install Python dependencies: `pip install streamlit langchain-ollama`
4. Run the Streamlit app: `streamlit run app.py`
'''
import streamlit as st
from backend import OllamaModel, MODEL_NAME # Import from backend

# Attempt to initialize the Ollama model via the backend
try:
    ollama_model_service = OllamaModel() # Use the class from backend.py
except Exception as e:
    st.error(f"Failed to initialize Ollama model ({MODEL_NAME}): {e}")
    st.error("Please ensure Ollama is running, the model is pulled (e.g., `ollama pull phi3.5:latest`), and backend.py is in the same directory.")
    st.stop()

# Streamlit app UI
st.set_page_config(page_title="Local LLM Chat with Ollama", layout="wide")

st.title("💬 Chat with your Local LLM via Ollama")
st.caption(f"Powered by Ollama, LangChain, and Streamlit, using model: `{MODEL_NAME}`")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user prompt
prompt = st.chat_input("Ask the LLM anything...")

if prompt:
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from LLM using the backend service
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Placeholder for streaming response
        full_response = ""
        try:
            # Stream the response from the LLM via backend
            for chunk in ollama_model_service.get_response_stream(prompt):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌") # Add a cursor effect
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except ConnectionError as ce:
            error_message = f"Connection Error: {ce}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.info("Please check if the backend is running correctly and the Ollama server is accessible.")
        except Exception as e:
            error_message = f"Error communicating with Ollama via backend: {e}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.info("Ensure Ollama is running and the model is available. You might need to run `ollama serve` in your terminal if it's not started automatically, and `ollama pull {MODEL_NAME}`.")
