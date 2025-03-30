import os
import sys
import threading
import time
import psutil
import logging
import shutil
import openai
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

# Add the `CodeBot` directory to the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# Import modules from the new structure
from core.self_improvement import run_genetic_algorithm, analyze_logs
from core.ai_engine import explain_python_code
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import handle_exception  # Updated import
from modules.file_manager import setup_project_structure

# Configure logging
LOG_FILE = os.path.join(BASE_DIR, "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()

# ------------------
# CHATBOT CLASS
# ------------------
class Chatbot:
    def __init__(self):
        logger.info("Chatbot initialized.")

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
                elif command.startswith("run genetic algorithm"):
                    source_file = os.path.join(BASE_DIR, "example.py")
                    output_dir = os.path.join(BASE_DIR, "genetic_population")
                    run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
                else:
                    console.print(Panel("Unknown command. Type 'help' for a list of commands.", title="Error"))
            except Exception as e:
                logger.error(f"Chatbot error: {e}")

# ------------------
# UI FUNCTIONS
# ------------------
def display_menu():
    logger.info("Displaying main menu.")
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
    logger.info(f"Handling menu choice: {choice}")
    if choice == "1":
        chatbot = Chatbot()
        chatbot.start()
    elif choice == "2":
        source_file = os.path.join(BASE_DIR, "example.py")
        output_dir = os.path.join(BASE_DIR, "genetic_population")
        run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
    elif choice == "3":
        log_file = os.path.join(BASE_DIR, "logs", "codebot_genetic.log")
        summary = analyze_logs(log_file)
        print(summary)  # Display the summary to the user
    elif choice == "4":
        manage_iterations()
    elif choice == "5":
        setup_project_structure(BASE_DIR)
        console.print(Panel("Project structure setup completed successfully.", title="Success"))
    elif choice == "6":
        console.print(Panel("Exiting CodeBot. Goodbye!", title="Exit"))
        sys.exit(0)
    else:
        console.print(Panel("Invalid choice. Please try again.", title="Error"))

# ------------------
# CORE FUNCTIONS
# ------------------
def monitor_resources(interval=5):
    logger.info("Started monitoring system resources.")
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
    logger.info(f"Clearing folder: {folder_path}")
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        logger.info(f"Cleared and recreated folder: {folder_path}")
    except Exception as e:
        handle_exception(logger, f"Error clearing folder {folder_path}", e)


def handle_command(command):
    logger.info(f"Handling command: {command}")
    command = sanitize_input(command)

    if command.startswith("explain python"):
        code_snippet = command.replace("explain python", "").strip()
        if not code_snippet:
            return "Error: Please provide a Python code snippet to explain."
        return explain_python_code(code_snippet)
    # Other commands...


def handle_inject_command():
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

def ai_suggested_improvement(code):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Suggest improvements for the following Python code:\n{code}",
        max_tokens=150
    )
    return response["choices"][0]["text"]

# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    logger.info("CodeBot Core started.")
    console.print("[bold green]CodeBot Core is running![/bold green]")
    
    while True:
        display_menu()
        choice = Prompt.ask("Enter your choice")
        handle_menu_choice(choice)