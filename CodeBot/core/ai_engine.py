from transformers import pipeline
from typing import Generator

# Global variable for the text-generation model
generator = None

def preload_model():
    """
    Preloads the Hugging Face text-generation model to improve runtime performance.
    """
    global generator
    if generator is None:
        try:
            print("Loading AI model...")
            generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading AI model: {e}")

# Preload the model at the start of the program
preload_model()

def explain_python_code(code_snippet):
    """
    Explains the given Python code using the Hugging Face AI model.

    Args:
        code_snippet (str): The Python code snippet to explain.

    Returns:
        str: The explanation of the code or an error message.
    """
    global generator
    if generator is None:
        return "AI model is not loaded. Please preload the model."

    try:
        response = generator(f"Explain this Python code: {code_snippet}", max_length=100, num_return_sequences=1)
        if response and isinstance(response, list) and 'generated_text' in response[0]:
            return response[0]['generated_text']
        return "Unexpected response format from the AI model."
    except Exception as e:
        return f"Error generating explanation: {e}"
    
# Debugging
if __name__ == "__main__":
    print("DEBUG: Testing explain_python_code")
    sample_code = "def greet(name): return f'Hello, {name}!'"
    explanation = explain_python_code(sample_code)
    print(f"Input Code:\n{sample_code}\n")
    print(f"Generated Explanation:\n{explanation}")