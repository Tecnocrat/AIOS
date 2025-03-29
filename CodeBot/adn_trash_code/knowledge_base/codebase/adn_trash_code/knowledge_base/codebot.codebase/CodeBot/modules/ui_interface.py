# Imports
import sys
import tkinter as tk
from tkinter import scrolledtext
from modules.dictionaries import word_recognition, suggest_word
from modules.file_manager import scan_test_folder
from modules.knowledge_base import retrieve_python_concept, save_conversation_to_log, inject_text
from modules.ai_engine import explain_python_code

# Add CodeBot folder to Python search path
sys.path.append("C:\\dev\\CodeBot")

# Optional import for resource monitoring
try:
    from modules.resources import monitor_resources
except ImportError:
    monitor_resources = None  # Skip monitoring if the module is unavailable

# Global Variables
CONVERSATION_LOG_PATH = "C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"
quit_flag = False  # Global flag to exit the app

# Logging
def collect_feedback(query, response):
    """
    Logs user feedback for AI responses.
    """
    feedback = input(f"Rate the response to \"{query}\" (1-5): ")
    with open("feedback_log.txt", "a") as log:
        log.write(f"Query: {query}\nResponse: {response}\nFeedback: {feedback}\n\n")

# UI Setup
def launch_ui():
    """
    Launches the UI interface for CodeBot.
    """
    root.mainloop()  # Start the tkinter UI

# Input Handling
def handle_input(event=None):
    """
    Handles user input, processes CodeBot's response, appends both to the chat history,
    and backs up interactions into the conversation log.
    """
    global quit_flag

    user_text = user_entry.get().strip().lower()
    user_entry.delete(0, tk.END)  # Clear the input field

    if quit_flag:
        root.quit()  # Exit application immediately
        return

    if not user_text:
        response = "CodeBot: Please enter a message."
    elif user_text in ["quit"]:
        quit_flag = True
        response = "CodeBot: Goodbye!"
    elif monitor_resources and user_text in ["monitor"]:
        response = monitor_resources()  # Perform resource monitoring if available
    elif user_text in ["hello", "hi", "hey", "greetings"]:
        response = "CodeBot: Hello, I'm CodeBot!"
    elif user_text.startswith("explain python"):
        # Explain a Python code snippet
        code_snippet = user_text.replace("explain python", "").strip()
        response = explain_python_code(code_snippet)
    elif user_text.startswith("explain"):
        # Retrieve a Python concept
        concept = user_text.replace("explain", "").strip()
        response = retrieve_python_concept(concept)
    elif user_text.startswith("inject knowledge"):
        # Inject knowledge into a specified file
        response = handle_inject_knowledge(user_text)
    elif user_text.endswith("?"):
        # Respond to Python-related questions dynamically
        response = "CodeBot: That's an interesting question. Let me think about it!"
    else:
        # Use word recognition
        response = handle_word_recognition(user_text)

    # Append user input and response to chat history
    output_area.insert(tk.END, f"You: {user_text}\n{response}\n")

    # Save conversation to log
    save_conversation_to_log(f"You: {user_text}\n{response}", log_path=CONVERSATION_LOG_PATH)

def handle_inject_knowledge(user_text):
    """
    Handles the 'inject knowledge' command to inject text into a file.
    """
    parts = user_text.replace("inject knowledge", "").strip().split(";")
    file_path = parts[0].strip() if len(parts) > 0 else None
    text = parts[1].strip() if len(parts) > 1 else None
    if file_path and text:
        inject_text(file_path, text, "append")
        return f"CodeBot: Injected knowledge into {file_path}."
    return "CodeBot: Invalid injection command."

def handle_word_recognition(user_text):
    """
    Handles word recognition and provides suggestions for recognized words.
    """
    recognized = word_recognition(user_text)
    if recognized:
        response = f"CodeBot: I recognized these words: {', '.join(recognized)}"
        suggestions = suggest_word(list(recognized)[0])
        if suggestions:
            response += f"\nCodeBot: Here are some word suggestions: {', '.join(suggestions)}"
        return response
    return "CodeBot: I didn't recognize any valid words. Try again!"

# Create the main UI window
root = tk.Tk()
root.title("CodeBot Chat")

# Create a scrolled text area for output
output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Helvetica", 12))
output_area.pack(pady=10)

# Create an entry widget for user input
user_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
user_entry.pack(pady=10)
user_entry.bind("<Return>", handle_input)  # Enter key triggers the function

# Create a button to send input
send_button = tk.Button(root, text="Send", command=handle_input, font=("Helvetica", 12))
send_button.pack(pady=10)

# Run the UI loop
launch_ui()