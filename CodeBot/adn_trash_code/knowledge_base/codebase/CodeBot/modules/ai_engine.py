from transformers import pipeline

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
        return "Error: AI model is not loaded. Please ensure the model is initialized."

    try:
        # Generate an explanation for the Python code snippet
        response = generator(
            f"Explain the following Python code:\n{code_snippet}",
            max_length=100,
            truncation=True
        )
        return response[0]["generated_text"]
    except Exception as e:
        return f"Error with AI engine: {e}"

        # Check for repetitive or incomplete outputs
        if "def" in generated_text and len(set(generated_text.split())) < 15:
            return "AI Explanation: The response seems repetitive. Consider refining the query."

        return generated_text
    except Exception as e:
        return f"Error with AI engine: {e}"