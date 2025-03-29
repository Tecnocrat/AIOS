import os
import sys
import threading
import time
import psutil
import logging
import shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt

# Add CodeBot folder to Python search path
CODEBOT_DIR = os.path.dirname(os.path.abspath(__file__))
ADB_DIR = os.path.join(os.path.dirname(CODEBOT_DIR), "adn_trash_code")
os.makedirs(ADB_DIR, exist_ok=True)

MODULES_DIR = os.path.join(CODEBOT_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.append(MODULES_DIR)

# Import modules
from self_improvement import run_genetic_algorithm
from log_analysis import analyze_logs
from iteration_manager import manage_iterations
from modules.file_manager import setup_project_structure, scan_test_folder, inject_text
from modules.compression import compress_libraries, decompress_library
from modules.knowledge_base import create_knowledge_archive, save_knowledge, retrieve_python_concept
from modules.ui_interface import launch_ui
from modules.dictionaries import save_wordlists
from modules.learning import load_language_libraries, analyze_library, copy_core_for_testing
from modules.ai_engine import explain_python_code
from modules.text_injector import inject_text as custom_inject_text
from modules.utils import sanitize_input, get_valid_file_path, handle_exception

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()
console.print("Rich library is working!")

# ------------------
# CHATBOT CLASS
# ------------------
class Chatbot:
    def __init__(self):
        self.running = True

    def start(self):
        logger.info("Chatbot started.")
        console.print(Panel("Welcome to CodeBot Chatbot! Type 'help' for commands.", title="Chatbot"))
        while self.running:
            try:
                command = Prompt.ask("You")
                if command.strip().lower() == "quit":
                    self.running = False
                elif command.startswith("explain python"):
                    code_snippet = command.replace("explain python", "").strip()
                    response = explain_python_code(code_snippet)
                    console.print(Panel(response, title="CodeBot"))
                else:
                    console.print(Panel("Unknown command. Type 'help' for a list of commands.", title="Error"))
            except Exception as e:
                logger.error(f"Chatbot error: {e}")

# ------------------
# UI FUNCTIONS
# ------------------
def display_menu():
    """
    Displays the main menu with options for all functions.
    """
    table = Table(title="CodeBot Command Panel")
    table.add_column("Option", justify="center", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("1", "Run Chatbot")
    table.add_row("2", "Run Self-Improvement")
    table.add_row("3", "Run Log Analysis")
    table.add_row("4", "Run Iteration Manager")
    table.add_row("5", "Setup Project Structure")
    table.add_row("6", "Exit")

    console.print(table)

def handle_menu_choice(choice):
    """
    Handles the user's menu choice.
    """
    if choice == "1":
        chatbot = Chatbot()
        chatbot.start()
    elif choice == "2":
        source_file = os.path.join(CODEBOT_DIR, "example.py")
        output_dir = os.path.join(CODEBOT_DIR, "genetic_population")
        run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
    elif choice == "3":
        log_file = os.path.join(CODEBOT_DIR, "logs", "codebot_genetic.log")
        analyze_logs(log_file)
    elif choice == "4":
        manage_iterations()
    elif choice == "5":
        setup_project_structure(CODEBOT_DIR)
    elif choice == "6":
        console.print(Panel("Exiting CodeBot. Goodbye!", title="Exit"))
        sys.exit(0)
    else:
        console.print(Panel("Invalid choice. Please try again.", title="Error"))

# ------------------
# CORE FUNCTIONS
# ------------------
def monitor_resources(interval=5):
    """
    Monitors system resources (CPU, memory, and disk usage) and logs the data periodically.
    """
    logger.info("Starting resource monitoring...")
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            logger.info(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory}% | Disk Usage: {disk}%")
            time.sleep(interval)
    except Exception as e:
        handle_exception(logger, "Error monitoring resources", e)


def clear_folder(folder_path):
    """
    Deletes all contents of the specified folder and recreates it.
    """
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        logger.info(f"Cleared and recreated folder: {folder_path}")
    except Exception as e:
        handle_exception(logger, f"Error clearing folder {folder_path}", e)


def handle_command(command):
    """
    Handles user commands and executes corresponding actions.

    Args:
        command (str): The user input command.

    Returns:
        str: The response to the command.
    """
    logger.debug(f"Received command: {command}")
    command = sanitize_input(command)

    if command.startswith("explain python"):
        # Extract the Python code snippet from the input
        code_snippet = command.replace("explain python", "").strip()
        if not code_snippet:
            return "Error: Please provide a Python code snippet to explain."
        return explain_python_code(code_snippet)
    # Other commands...


def handle_inject_command():
    """
    Handles the 'inject' command to inject text into a file.
    """
    try:
        file_path = get_valid_file_path("Enter file path: ")
        text = input("Enter text to inject: ").strip()
        position = sanitize_input(input("Enter injection mode (append/overwrite/insert): "))
        line_number = None
        if position == "insert":
            try:
                line_number = int(input("Enter line number for insertion: "))
            except ValueError:
                return "Invalid line number."
        result = inject_text(file_path, text, position, line_number)
        return result
    except Exception as e:
        return handle_exception(logger, "Error handling inject command", e)


# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    while True:
        display_menu()
        choice = Prompt.ask("Enter your choice")
        handle_menu_choice(choice)