'''
Backend logic for interacting with the Ollama model.
'''
from langchain_ollama.chat_models import ChatOllama

MODEL_NAME = "phi3.5:latest"  # As requested

class OllamaModel:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.llm = None
        self._initialize_model()

    def _initialize_model(self):
        try:
            self.llm = ChatOllama(model=self.model_name)
            print(f"Successfully initialized Ollama model: {self.model_name}")
        except Exception as e:
            print(f"Error in backend: Failed to initialize Ollama model ({self.model_name}): {e}")
            # Re-raise the exception so the frontend can catch it and display an error
            raise

    def get_response_stream(self, prompt: str):
        if not self.llm:
            raise ConnectionError("Ollama model not initialized. Please check backend logs.")
        try:
            return self.llm.stream(prompt)
        except Exception as e:
            print(f"Error in backend: Failed to get response stream from Ollama: {e}")
            # Re-raise or handle as appropriate for your error strategy
            raise

# Example of how to use it (optional, for testing backend independently)
if __name__ == '''__main__''':
    try:
        ollama_model = OllamaModel()
        test_prompt = "Hello, who are you?"
        print(f"Sending prompt to {MODEL_NAME}: {test_prompt}")
        response_stream = ollama_model.get_response_stream(test_prompt)
        print(f"Response from {MODEL_NAME}:")
        for chunk in response_stream:
            print(chunk.content, end="", flush=True)
        print()
    except Exception as e:
        print(f"Failed to run backend test: {e}")
