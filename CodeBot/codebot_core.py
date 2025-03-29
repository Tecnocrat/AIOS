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

# Base directory for all operations
BASE_DIR = "c:\\dev"
CODEBOT_DIR = os.path.join(BASE_DIR, "CodeBot")
ADN_TRASH_CODE_DIR = os.path.join(CODEBOT_DIR, "adn_trash_code")
KNOWLEDGE_BASE_DIR = os.path.join(CODEBOT_DIR, "knowledge_base")
MODULES_DIR = os.path.join(CODEBOT_DIR, "modules")

# Ensure critical directories exist
os.makedirs(ADN_TRASH_CODE_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
if MODULES_DIR not in sys.path:
    sys.path.append(MODULES_DIR)

# Configure logging
LOG_FILE = os.path.join(CODEBOT_DIR, "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w"),  # Overwrite log file on each run
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